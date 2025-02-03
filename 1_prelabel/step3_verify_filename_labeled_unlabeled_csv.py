#!/usr/bin/python3


import csv
'''
Verifica la primeira columna de cada arquivo csv e logo mostra 
    * quais elementos estao no arquivo 1 e nao no arquivo 2 e 
    * quais elementos estao no arquivo 2 e nao no arquivo 1
'''
def comparar_csvs(arquivo1, arquivo2):
    # Lê a primeira coluna de cada arquivo e armazena os valores em sets
    with open(arquivo1, 'r', encoding='utf-8') as f1, open(arquivo2, 'r', encoding='utf-8') as f2:
        leitor1 = csv.reader(f1)
        leitor2 = csv.reader(f2)

        # Ignora o cabeçalho
        cabecalho1 = next(leitor1, None)
        cabecalho2 = next(leitor2, None)

        col1_arquivo1 = [linha[0] for linha in leitor1]
        col1_arquivo2 = [linha[0] for linha in leitor2]

    # Converte para conjuntos para identificar elementos únicos
    set1 = set(col1_arquivo1)
    set2 = set(col1_arquivo2)

    # Elementos presentes apenas em cada arquivo
    apenas_no_arquivo1 = set1 - set2
    apenas_no_arquivo2 = set2 - set1

    # Imprime os resultados
    print(f"Elementos diferentes no arquivo {arquivo1}: {apenas_no_arquivo1}")
    print(f"Elementos diferentes no arquivo {arquivo2}: {apenas_no_arquivo2}")

    # Encontra e imprime as linhas que são diferentes
    for i, valor in enumerate(col1_arquivo1):
        if valor in apenas_no_arquivo1:
            print(f"Diferença no arquivo {arquivo1} na linha {i + 2}: {valor}")

    for i, valor in enumerate(col1_arquivo2):
        if valor in apenas_no_arquivo2:
            print(f"Diferença no arquivo {arquivo2} na linha {i + 2}: {valor}")

########################################################################

# Substitua pelos nomes dos seus arquivos CSV
arquivo_csv1 = '../labeled_files.csv'
arquivo_csv2 = '/mnt/8811f502-ae19-4dd8-8371-f1915178f581/Fernando/DATASET/TESE/PER/PER2024-SOURCE/unlabeled_files.csv'

comparar_csvs(arquivo_csv1, arquivo_csv2)

