#!/usr/bin/python3

INPUT_DIR  = '/mnt/8811f502-ae19-4dd8-8371-f1915178f581/Fernando/DATASET/TESE/PER/PER2024-SOURCE'
INPUT_FILE = 'unlabeled_files.csv'

OUTPUT_DIR  = '/mnt/8811f502-ae19-4dd8-8371-f1915178f581/Fernando/DATASET/TESE/PER/PER2024-SOURCE'
OUTPUT_FILE = 'prelabeled_files.csv'


checkpoint='shufflenetv2k16';
model_type_face='efficientnet_b3';
model_type_body='efficientnet_b3';
model_type_skel=20;
model_type_skel_enable_minus=True;
model_type_fusion=7;
body_factor=1.0;
face_factor=0.85;
face_detector_method=1;

################################################################################
import json
import os
import hashlib

INFO=dict();
INFO["model_type_body"] = model_type_body;
INFO["model_type_face"] = model_type_face;
INFO["model_type_skel"] = model_type_skel;
INFO["model_type_fusion"] = model_type_fusion;
INFO["enable_minus"] = model_type_skel_enable_minus;
INFO['body_factor'] = body_factor;
INFO['face_factor'] = face_factor;
INFO['face_detector_method'] = face_detector_method;

# Serializar o dicionário em uma string JSON com uma ordenação consistente
json_string = json.dumps(INFO, sort_keys=True)
# Gerar um hash MD5 a partir da string JSON
hash_object = hashlib.md5(json_string.encode())
pre_name = hash_object.hexdigest()

print("pre_name:",pre_name)
processed_json_path = os.path.join(OUTPUT_DIR,pre_name+'_'+OUTPUT_FILE+'.json');

# Salvando o dicionário em um arquivo JSON
with open(processed_json_path, 'w') as arquivo_json:
    json.dump(INFO, arquivo_json, indent=4)

################################################################################


## Because the KERAS used is a old verion, KERAS 1
os.environ['TF_USE_LEGACY_KERAS'] = '1'

## Allows memory allocation on the GPU to be done asynchronously, 
## potentially improving performance and efficiency in certain scenarios.
os.environ['TF_GPU_ALLOCATOR'] = 'cuda_malloc_async'

## Specify which GPUs are available to a program.
## The list of GPUs is usually represented by indices starting at 0.
#os.environ['CUDA_VISIBLE_DEVICES'] = '-1' # disable cuda

import sys

from PIL import Image
import SystemEmotion4Lib.tools_funcs as toolf
import SystemEmotion4Lib.Classifier as sec
import tensorflow as tf
import pandas as pd
from natsort import natsorted

print("GPUs available: ", len(tf.config.experimental.list_physical_devices('GPU')))


cls=sec.Emotion4Classifier( checkpoint=checkpoint,
                            model_type_face=model_type_face,
                            model_type_body=model_type_body,
                            model_type_skel=model_type_skel,
                            model_type_skel_enable_minus=model_type_skel_enable_minus,
                            model_type_fusion=model_type_fusion,
                            body_factor= body_factor,
                            face_factor=face_factor,
                            face_detector_method=face_detector_method);

print("")
print("System loaded")
print("")


def find_unprocessed_data(all_files_csv_path, processed_csv_path):
    # Carregue os dados dos arquivos CSV
    df_all_files = pd.read_csv(all_files_csv_path)
    
    # Verifique se o arquivo de processados existe
    if not os.path.isfile(processed_csv_path):
        return df_all_files, len(df_all_files)

    df_processed = pd.read_csv(processed_csv_path)

    # Certifique-se de que as colunas 'body' são strings
    df_all_files['body'] = df_all_files['body'].astype(str)
    df_processed['body'] = df_processed['body'].astype(str)

    # Crie conjuntos com os caminhos dos arquivos
    all_files_set = set(df_all_files['body'])
    processed_set = set(df_processed['body'])

    # Contando a frequência de cada elemento na coluna 'body'
    frequencias_all = df_all_files['body'].value_counts()
    frequencias_pro = df_processed['body'].value_counts()
    
    elementos_duplicados_all = frequencias_all[frequencias_all > 1];
    elementos_duplicados_pro = frequencias_pro[frequencias_pro > 1];
    
    if len(elementos_duplicados_all)>0:
        print("")
        print("**************************************************")
        print("Deves corrigir os seguintes arquivos duplicados em",all_files_csv_path)
        print(elementos_duplicados_all)
        exit();
    
    if len(elementos_duplicados_pro)>0:
        print("")
        print("**************************************************")
        print("Deves corrigir os seguintes arquivos duplicados em",processed_csv_path)
        print(elementos_duplicados_pro)
        exit();

    # Calcule a diferença entre os conjuntos
    missing_data = all_files_set - processed_set
    
    print("")
    print("    The input cvs file tem",len(all_files_set),"different elements.");
    print("The processed cvs file tem",len(processed_set),"different elements.");
    
    if len(missing_data)==0:
        print("")
        print("**************************")
        print("O trabalho ja estava feito")
        return pd.DataFrame(columns=['body','face','skeleton']), len(df_all_files)

    # Filtre o DataFrame original para obter os dados que faltam processar
    missing_df = df_all_files[df_all_files['body'].isin(missing_data)]

    # Ordene o DataFrame usando natural sorting na coluna 'body'
    #missing_df['body']        = missing_df['body'].apply(str)
    missing_df.loc[:, 'body'] = missing_df['body'].apply(str)

    sorted_missing_df = missing_df.reindex(natsorted(missing_df['body'].index)).reset_index(drop=True)

    return sorted_missing_df, len(df_all_files)

def my_batch_func(batch):
    
    img_pil_list=[];
    for item in batch:
        filepath=item[0];
        img_pil_list.append(Image.open(filepath));

    res=cls.from_img_pil_list(img_pil_list);
    
    words = ['negative', 'neutro', 'pain', 'positive']
    
    return [words[ID] for ID in res];

################################################################################

if __name__=="__main__":

    print('')

    input_csv_path     = os.path.join(INPUT_DIR,INPUT_FILE);
    processed_csv_path = os.path.join(OUTPUT_DIR,pre_name+'_'+OUTPUT_FILE);

    print('Input working in csv:',input_csv_path);
    print('       Processed csv:',processed_csv_path);

    missing_df, total_length = find_unprocessed_data(input_csv_path, processed_csv_path);
    
    print('')
    print('missing_length:',len(missing_df));
    print('  total_length:',total_length);

    if len(missing_df)==0:
        print('')
        pass;
    else:
        print(missing_df)
        print('')

        # Função para adicionar o diretório base a cada valor
        missing_df = missing_df.astype(str).map(lambda path: f'{INPUT_DIR}/{path}')


        missing_list = list(missing_df.itertuples(index=False, name=None));
        print(len(missing_list),'of',total_length);

        print("Start cleaning")
        tf.keras.backend.clear_session()
        import torch
        torch.cuda.empty_cache()
        print("Cleaning End")
        
        toolf.save_dataset_list_in_csv_batch(INPUT_DIR,missing_list,processed_csv_path,my_batch_func,batch_size=32)

