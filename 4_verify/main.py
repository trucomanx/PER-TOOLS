#!/usr/bin/python3

import os
import pandas as pd

def verify_files_exist(csv_path, base_directory):
    """
    Verifica se todos os arquivos especificados na coluna 'filename' de um CSV existem.
    
    :param csv_path: Caminho para o arquivo CSV.
    :param base_directory: Diretório base para construir os caminhos completos.
    :return: Uma lista de caminhos que não existem. Se vazia, todos os arquivos existem.
    """
    # Carregar o CSV
    df = pd.read_csv(csv_path)
    
    # Verificar se a coluna 'filename' existe
    if 'filename' not in df.columns:
        raise ValueError("O arquivo CSV não contém a coluna 'filename'.")
    
    # Lista para armazenar arquivos inexistentes
    missing_files = []
    
    # Iterar sobre os caminhos relativos
    for relative_path in df['filename']:
        full_path = os.path.join(base_directory, relative_path)
        if not os.path.exists(full_path):
            missing_files.append(full_path)
            
    print(csv_path)
    
    if missing_files:
        print("Os seguintes arquivos estão ausentes:")
        for file in missing_files:
            print(file)
    else:
        print("Todos os arquivos existem!")
    
    return missing_files

# Exemplo de uso
if __name__ == "__main__":
    
    base_directory = "/mnt/8811f502-ae19-4dd8-8371-f1915178f581/Fernando/DATASET/TESE/PER/PER2024-SOURCE/"  
    
    csv_path_list = ["test_body.csv","test_face.csv","test_skeleton_npy.csv","train_body.csv","train_face.csv","train_skeleton_npy.csv"]
    
    for csv_path in csv_path_list:
        path_full=os.path.join(base_directory,csv_path)
        missing_files = verify_files_exist(path_full, base_directory)
    
