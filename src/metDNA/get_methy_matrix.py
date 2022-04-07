import pandas as pd
from glob import glob
from tqdm import tqdm
import numpy as np

sample_sheet = pd.read_csv('sample_sheet_450.csv')
labels = {}
data = pd.DataFrame()
for _,row in tqdm(sample_sheet.iterrows()):
    case_id = row['Sample ID']
    file = glob('Methy/'+case_id+'/jhu*.txt')[0]
    df = pd.read_csv(file, sep='\t')
    try:
    	data[case_id] = df['Beta_value'].values
    except:
        print('Error in file {}'.format(case_id))
        print(df.shape)
        pass
    label = row['Project ID']
    if '11A' in case_id:
        labels[case_id] = 'Healthy'
    elif label == 'TCGA-LUAD':
        labels[case_id] = 'LUAD'
    elif label == 'TCGA-LUSC':
        labels[case_id] = 'LUSC'



cpgs = df['Composite Element REF'].values
cpgs = np.append(cpgs, 'Label')
data = data.append(labels, ignore_index=True)
data.insert(0, 'CpGs', cpgs)
data.to_csv('CpGs_450_matrix.csv', index=False, sep=',')
