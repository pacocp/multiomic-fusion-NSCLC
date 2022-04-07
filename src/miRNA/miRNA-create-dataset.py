import pandas as pd
import tqdm
import argparse

# parse arguments
parser = argparse.ArgumentParser(description='Create dataset \
                                 for RNA-seq data.')
parser.add_argument('--name', dest='csv_name', type=str, default='dataset',
                    help="name for the csv to be saved. Don't need to put the \
                          extension")
parser.add_argument('--sample_sheet', dest='sample_sheet', type=str,
                    default='sample_sheet',
                    help="name for the sample_sheet in csv format. Don't need to \
                          put the extension")
parser.add_argument('--clinical', dest='clinical_name', type=str,
                    default='clinical',
                    help="name for the clinical in tsv format. Don't need to \
                          put the extension")
parser.add_argument('--path', dest='path', type=str,
                    default='expression',
                    help="path to expression files")

args = parser.parse_args()

stage_iorii = ['stage i', 'stage ia', 'stage ib', 'stage ii', 'stage iia',
               'stage iib']
stage_iiioriv = ['stage iii', 'stage iiia', 'stage iiib', 'stage iv']

X = []
Y = []

data = pd.read_csv(args.sample_sheet + '.csv', sep=',')
clinical = pd.read_csv(args.clinical_name + '.tsv', sep='\t')
sample_id = []
for index, row in tqdm.tqdm(data.iterrows()):
    file_path = args.path + '/' + row['Sample ID'] + '/' + row['Sample ID'] + '.txt'
    data_values = pd.read_csv(file_path, sep='\t')
    #try:
    label_start = row['Sample ID'].split('-')[-1]
    if label_start[0] == '1':
        continue
    elif label_start[0] == '0':
        row_clinical = clinical.loc[clinical['case_submitter_id'] == row['Case ID']]
        if row_clinical['tumor_stage'].values[0] in stage_iorii:
            Y.append('early')
            data_values = data_values[['miRNA_ID', 'read_count']]
            X.append(data_values.values.T[1])
            sample_id.append(row['Sample ID'])
        elif row_clinical['tumor_stage'].values[0] in stage_iiioriv:
            Y.append('advanced')
            data_values = data_values[['miRNA_ID', 'read_count']]
            X.append(data_values.values.T[1])
            sample_id.append(row['Sample ID'])
    '''
    except Exception:
        print(file_path)
        continue
    '''

dataset = pd.DataFrame()
dataset['Case_ID'] = sample_id
values_ = pd.DataFrame(X, columns=data_values.values.T[0])
dataset = pd.concat([dataset, values_], axis=1)
dataset['Labels'] = Y
dataset.to_csv(args.csv_name + '.csv', index=False, sep=',')
