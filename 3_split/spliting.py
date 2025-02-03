#!/usr/bin/python3

import pandas as pd
from sklearn.model_selection import train_test_split
from collections import Counter
import json
import os
import random
import numpy as np

def carregar_csv_sem_erros(arquivo_csv,label_name='label',error_name='error'):
    """
    Lê um arquivo CSV e carrega em um DataFrame, ignorando as linhas
    onde a coluna label_name contém o valor error_name.

    :param arquivo_csv: Caminho para o arquivo CSV.
    :return: DataFrame sem as linhas com error_name na coluna label_name.
    """
    # Lê o CSV em um DataFrame
    df = pd.read_csv(arquivo_csv)
    
    # Filtra as linhas onde a coluna label_name não é error_name
    if label_name in df.columns:
        df = df[df[label_name] != error_name]
    else:
        raise ValueError("A coluna label_name não foi encontrada no arquivo CSV.")
    
    return df


def dividir_dataframe(dataframe, fator_treino=0.8, coluna_label='label',random_state=42):
    """
    Divide um DataFrame em dois (treinamento e teste) mantendo a proporção
    dos elementos na coluna especificada.

    :param dataframe: DataFrame original.
    :param fator_treino: Proporção de linhas para o conjunto de treinamento (0 a 1).
    :param coluna_label: Nome da coluna que será usada para estratificação.
    :return: Dois DataFrames, (treinamento, teste).
    """
    if coluna_label not in dataframe.columns:
        raise ValueError(f"A coluna '{coluna_label}' não foi encontrada no DataFrame.")
    
    # Divisão estratificada
    df_treino, df_teste = train_test_split(
        dataframe, 
        train_size=fator_treino, 
        stratify=dataframe[coluna_label],
        random_state=random_state  # Para resultados reproduzíveis
    )
    
    return df_treino, df_teste


def obter_estatisticas_label(dataframe, filepath,coluna_label='label'):
    """
    Calcula a estatística das categorias em uma coluna específica de um DataFrame.

    :param dataframe: DataFrame contendo os dados.
    :param coluna_label: Nome da coluna a ser analisada.
    :return: JSON contendo as estatísticas das categorias.
    """
    if coluna_label not in dataframe.columns:
        raise ValueError(f"A coluna '{coluna_label}' não foi encontrada no DataFrame.")
    
    # Contar as ocorrências das categorias
    contador = Counter(dataframe[coluna_label])
    
    # Converter o resultado para JSON
    #print(json.dumps(dict(contador), ensure_ascii=False, indent=4, sort_keys=True))
    
    with open(filepath, 'w', encoding='utf-8') as arquivo_json:
        json.dump(dict(contador), arquivo_json, ensure_ascii=False, indent=4, sort_keys=True)
    
    return dict(contador)

def convert_dataframe(df, base_path):
    """
    Converte um DataFrame com colunas 'filename' e 'label' em um DataFrame expandido.
    Carrega os vetores de arquivos .npy e adiciona colunas 'd0', 'd1', ..., 'd50', junto com 'label'.
    
    :param df: DataFrame com colunas ['filename', 'label'].
    :param base_path: Caminho base para os arquivos .npy.
    :return: Novo DataFrame com colunas ['d0', 'd1', ..., 'd50', 'label'].
    """
    # Lista para armazenar os dados processados
    data = []
    
    for _, row in df.iterrows():
        # Construa o caminho absoluto do arquivo .npy
        npy_path = os.path.join(base_path, row['filename'])
        
        # Carregue o vetor numpy
        vector = np.load(npy_path)
        vector[vector < 0.0] = 0.0
        
        if len(vector) != 51:
            raise ValueError(f"Vetor no arquivo {npy_path} não tem 51 elementos!")
        
        # Adicione os valores do vetor e o label à lista
        data.append(list(vector) + [row['label']])
    
    # Crie as colunas d0, d1, ..., d50 e label
    columns = [f"d{i}" for i in range(51)] + ["label"]
    
    # Retorne o novo DataFrame
    return pd.DataFrame(data, columns=columns)

def split_df_columns_face_body_skeleton(df,base_path):
    df_body     = df[['body', 'label']]
    df_body     = df_body.rename(columns={'body':'filename'})

    df_face     = df[['face', 'label']]
    df_face     = df_face.rename(columns={'face':'filename'})

    df_skeleton = df[['skeleton', 'label']]
    df_skeleton = df_skeleton.rename(columns={'skeleton':'filename'})
    
    df_skeleton_vec=convert_dataframe(df_skeleton, base_path)
    
    return df_face, df_body, df_skeleton, df_skeleton_vec

def save_dataframes_in_dir(df_body,df_face,df_skeleton_npy,df_skeleton,OUTDIR_FULL,pre_name="train"):
    df_body.to_csv(os.path.join(OUTDIR_FULL,pre_name+'_body.csv'), index=False, encoding='utf-8')
    df_face.to_csv(os.path.join(OUTDIR_FULL,pre_name+'_face.csv'), index=False, encoding='utf-8')
    df_skeleton_npy.to_csv(os.path.join(OUTDIR_FULL,pre_name+'_skeleton_npy.csv'), index=False, encoding='utf-8')
    df_skeleton.to_csv(os.path.join(OUTDIR_FULL,pre_name+'_skeleton.csv'), index=False, encoding='utf-8')

    obter_estatisticas_label(df_body,os.path.join(OUTDIR_FULL,pre_name+'.json'),coluna_label='label')


def dividir_indices(L, f):
    """
    Divide os índices de 0 a L-1 em dois grupos, seguindo a proporção f.
    
    :param L: Número total de elementos.
    :param f: Fração de índices para o primeiro grupo (entre 0 e 1).
    :return: Duas listas de índices (grupo1, complement).
    """
    if not (0 <= f <= 1):
        raise ValueError("A fração f deve estar entre 0 e 1.")
    
    # Criar a lista de índices
    total_indices = list(range(L))
    
    # Determinar o número de elementos no primeiro grupo
    num_grupo1 = int(L * f)
    
    # Selecionar aleatoriamente os índices para o primeiro grupo
    grupo1 = random.sample(total_indices, num_grupo1)
    
    # Determinar os índices restantes para o segundo grupo
    complement = list(set(total_indices) - set(grupo1))
    
    return grupo1, complement


def indices_a_eliminar(df,label_col='label',element='neutro',factor=0.1):
    indices_element = df[df[label_col] == element].index.tolist()
    list_id, list_complement = dividir_indices(len(indices_element), factor)
    
    return [indices_element[ID] for ID in list_id], [indices_element[ID] for ID in list_complement]
    
################################################################################
################################################################################


base_path='/mnt/8811f502-ae19-4dd8-8371-f1915178f581/Fernando/DATASET/TESE/PER/PER2024-SOURCE'
INPUT_FILE="../2_add_labels/labels_added.csv"
FACTOR_TREINO=0.618
FACTOR_DROP=0.06
OUTDIR_FULL='output_full'
OUTDIR_DROP='output_drop06'

random.seed(42)

# Exemplo de uso
df = carregar_csv_sem_erros(INPUT_FILE)

df_train, df_test = dividir_dataframe(df, fator_treino=FACTOR_TREINO, coluna_label='label',random_state=42)

df_train = df_train.reset_index()
df_test  = df_test.reset_index()

################################################################################

df_train_face, df_train_body, df_train_skeleton_npy, df_train_skeleton = split_df_columns_face_body_skeleton(df_train,base_path)
print(len(df_train_body),len(df_train_face),len(df_train_skeleton))

df_test_face, df_test_body, df_test_skeleton_npy, df_test_skeleton = split_df_columns_face_body_skeleton(df_test,base_path)
print(len(df_test_body),len(df_test_face),len(df_test_skeleton))

################################################################################

os.makedirs(OUTDIR_FULL,exist_ok=True)

save_dataframes_in_dir(df_train_body,df_train_face,df_train_skeleton_npy,df_train_skeleton,OUTDIR_FULL,pre_name="train")

save_dataframes_in_dir(df_test_body,df_test_face,df_test_skeleton_npy,df_test_skeleton,OUTDIR_FULL,pre_name="test")

################################################################################

id_element, id_complement=indices_a_eliminar(df_train,label_col='label',element='neutro',factor=FACTOR_DROP)
    
df_train_face         = df_train_face.drop(index=id_complement)
df_train_body         = df_train_body.drop(index=id_complement)
df_train_skeleton     = df_train_skeleton.drop(index=id_complement)
df_train_skeleton_npy = df_train_skeleton_npy.drop(index=id_complement)

id_element, id_complement=indices_a_eliminar(df_test,label_col='label',element='neutro',factor=FACTOR_DROP)
df_test_face         = df_test_face.drop(index=id_complement)
df_test_body         = df_test_body.drop(index=id_complement)
df_test_skeleton     = df_test_skeleton.drop(index=id_complement)
df_test_skeleton_npy = df_test_skeleton_npy.drop(index=id_complement)

os.makedirs(OUTDIR_DROP,exist_ok=True)

save_dataframes_in_dir(df_train_body,df_train_face,df_train_skeleton_npy,df_train_skeleton,OUTDIR_DROP,pre_name="train")

save_dataframes_in_dir(df_test_body,df_test_face,df_test_skeleton_npy,df_test_skeleton,OUTDIR_DROP,pre_name="test")


