import argparse
import pandas as pd
import json
import glob

# parse arguments
parser = argparse.ArgumentParser(description='Create dataset \
                                 for RNA-seq data.')
parser.add_argument('--name', dest='csv_name', type=str, default='dataset',
                    help="name for the csv to be saved. Don't need to put the \
                          extension")
parser.add_argument('--json', dest='json_name', type=str, default='metadata',
                    help="name for the metadata in json format. Don't need to \
                          put the extension")
parser.add_argument('--clinical', dest='clinical_name', type=str,
                    default='clinical',
                    help="name for the clinical in tsv format. Don't need to \
                          put the extension")

args = parser.parse_args()

squa = ['Basaloid squamous cell carcinoma',
        'Papillary squamous cell carcinoma',
        'Squamous cell carcinoma, NOS',
        'Squamous cell carcinoma, keratinizing, NOS',
        'Squamous cell carcinoma, large cell, nonkeratinizing, NOS',
        'Squamous cell carcinoma, small cell, nonkeratinizing']

adeno = ['Adenocarcinoma with mixed subtypes', 'Adenocarcinoma, NOS',
         'Bronchiolo-alveolar adenocarcinoma, NOS',
         'Bronchiolo-alveolar carcinoma, non-mucinous',
         'Clear cell adenocarcinoma, NOS', 'Micropapillary carcinoma, NOS',
         'Papillary adenocarcinoma, NOS', 'Solid carcinoma, NOS',
         'Bronchio-alveolar carcinoma, mucinous']


def get_submitter_id(case_id, data):
    for value in data:
        if(case_id == value['associated_entities'][0]['case_id']):
            return value['submitter_id']


def check_label(row, data, sample):
    """Check the label of the ID."""
    submitter_id = get_submitter_id(row['case_id'], data)
    print(submitter_id)
    count_name = submitter_id.split('_')[0] + '.htseq.counts.gz'
    label = sample['Sample Type'].loc[sample['File Name'] == count_name]
    return label.values[0]


def check_count_name(row, data):
    """Check count name of the ID."""
    submitter_id = get_submitter_id(row['case_id'], data)
    print(submitter_id)
    count_name = submitter_id.split('_')[0] + '.htseq.counts'
    return count_name


clinical = pd.read_csv(args.clinical_name + '.tsv', sep='\t')

with open(args.json_name + '.json') as json_file:
    data = json.load(json_file)

dataset = clinical
dataset['Count_Name'] = dataset.apply(lambda row: check_count_name(row, data),
                                      axis=1)
names_to_drop = []
labels = []
runs = []
paths_array = []
for label, name, stage in zip(dataset['primary_diagnosis'].values,
                              dataset['Count_Name'].values,
                              dataset['tumor_stage'].values):
    print(name)
    paths = glob.glob('counts/*/'+str(name))
    type_ = paths[0].split('/')[1].split('-')[-1]
    if type_[0] == '1':
        labels.append('healthy')
        paths_array.append(paths[0].split('/')[0] + '/' +
                           paths[0].split('/')[1])
        runs.append(paths[0].split('/')[1])
    elif type_[0] == '0':
        if label in squa:
            labels.append('squamous')
            paths_array.append(paths[0].split('/')[0] + '/' +
                               paths[0].split('/')[1])
            runs.append(paths[0].split('/')[1])
        elif label in adeno:
            labels.append('adeno')
            paths_array.append(paths[0].split('/')[0] + '/' +
                               paths[0].split('/')[1])
            runs.append(paths[0].split('/')[1])
        else:
            print('label not recognized for ')
            print(name)
            names_to_drop.append(name)
            print(label)

# create dataset for knowseq
mergedCounts = pd.DataFrame()
mergedCounts['Path'] = paths_array
mergedCounts['Run'] = runs
mergedCounts['Class'] = labels
mergedCounts.to_csv(args.csv_name+'.csv', sep=',', index=False)
