#!/usr/bin/python

import pandas as pd
import json
from collections import OrderedDict

def csv_to_json_summary(csv_path, json_path):
    # Lê o arquivo CSV
    df = pd.read_csv(csv_path)
    
    # Conta a quantidade de elementos por categoria
    category_counts = df['label'].value_counts().to_dict()
    
    # Ordena o dicionário por chave
    ordered_counts = OrderedDict(sorted(category_counts.items()))
    
    # Salva o resultado em um arquivo JSON
    with open(json_path, 'w') as json_file:
        json.dump(ordered_counts, json_file, indent=4)
    
    return dict(ordered_counts)


# Body
csv_path = '../PER2024-SOURCE/test_body.csv'
json_summary = csv_to_json_summary(csv_path, csv_path+'.json')
Ntest=sum(json_summary.values())
print('BODY-test :',json_summary,Ntest)

csv_path = '../PER2024-SOURCE/train_body.csv'
json_summary = csv_to_json_summary(csv_path, csv_path+'.json')
Ntrain=sum(json_summary.values())
print('BODY-train:',json_summary,Ntrain)

print(Ntest+Ntrain)

# Face
csv_path = '../PER2024-SOURCE/test_face.csv'
json_summary = csv_to_json_summary(csv_path, csv_path+'.json')
Ntest=sum(json_summary.values())
print('FACE-test :',json_summary,Ntest)

csv_path = '../PER2024-SOURCE/train_face.csv'
json_summary = csv_to_json_summary(csv_path, csv_path+'.json')
Ntrain=sum(json_summary.values())
print('FACE-train:',json_summary,Ntrain)

print(Ntest+Ntrain)

# Skel
csv_path = '../PER2024-SOURCE/test_skeleton.csv'
json_summary = csv_to_json_summary(csv_path, csv_path+'.json')
Ntest=sum(json_summary.values())
print('SKEL-test :',json_summary,Ntest)

csv_path = '../PER2024-SOURCE/train_skeleton.csv'
json_summary = csv_to_json_summary(csv_path, csv_path+'.json')
Ntrain=sum(json_summary.values())
print('SKEL-train:',json_summary,Ntrain)

print(Ntest+Ntrain)
