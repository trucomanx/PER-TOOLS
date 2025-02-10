#!/usr/bin/python3

import pandas as pd
import json
import os

def contar_labels(arquivo_csv, arquivo_json):
    # Carregar o arquivo CSV
    df = pd.read_csv(arquivo_csv)

    # Contar as ocorrências de cada label
    contagem = df["label"].value_counts().to_dict()

    # Salvar em um arquivo JSON
    with open(arquivo_json, "w") as f:
        json.dump(contagem, f, indent=4, sort_keys=True)

    print(f"✅ Estatísticas salvas em: {arquivo_json}")
    #print("✅",sum(contagem.values()),"/",len(df))
    
def combinar_csvs(arquivos, pasta_saida, nome_saida="resultado.csv"):
    # Carregar os arquivos CSV e concatenar em um único DataFrame
    dataframes = [pd.read_csv(arquivo) for arquivo in arquivos]
    df_final = pd.concat(dataframes, ignore_index=True)

    # Criar a pasta de saída se não existir
    os.makedirs(pasta_saida, exist_ok=True)

    # Caminho do arquivo de saída
    caminho_saida = os.path.join(pasta_saida, nome_saida)

    # Salvar o arquivo CSV final
    df_final.to_csv(caminho_saida, index=False)

    print(f"✅ Arquivo combinado salvo em: {caminho_saida}")



# Exemplo de uso

for input_type in ["ncod81_efficientnet_b3_efficientnet_b3", "ncod81_efficientnet_b3_efficientnet_b3_minus"]:
    for ds_type in ["train.csv", "test.csv"]:
        arquivos_csv = [
        os.path.join("full2024-fusion",input_type,ds_type),
        os.path.join("full2024-fusion-drop-face10",input_type,ds_type),
        os.path.join("full2024-fusion-drop-face25",input_type,ds_type)
        ]
        pasta_destino = os.path.join("full2024-fusion-drop-plus",input_type)
        combinar_csvs(arquivos_csv, pasta_destino, nome_saida=ds_type)
        
        
        contar_labels(  os.path.join(pasta_destino,ds_type), 
                        os.path.join(pasta_destino,ds_type+".json"))

