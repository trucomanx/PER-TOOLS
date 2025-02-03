import csv
import json
from collections import Counter


def agregar_coluna_label(arquivo1, arquivo2, arquivo_saida, label_col='label'):
    # Criar um dicionário com a primeira coluna como chave e a coluna "label" como valor
    dados_arquivo1 = {}
    with open(arquivo1, 'r', encoding='utf-8') as f1:
        leitor1 = csv.DictReader(f1)
        for linha in leitor1:
            chave = linha[leitor1.fieldnames[0]]  # Usa a primeira coluna como chave
            label = linha[label_col]  # Assume que há uma coluna chamada "label"
            dados_arquivo1[chave] = label

    # Adicionar a coluna "label" ao arquivo2
    with open(arquivo2, 'r', encoding='utf-8') as f2, open(arquivo_saida, 'w', encoding='utf-8', newline='') as f_saida:
        leitor2 = csv.DictReader(f2)
        # Adiciona a nova coluna "label" ao cabeçalho
        novos_campos = leitor2.fieldnames + [label_col]
        escritor = csv.DictWriter(f_saida, fieldnames=novos_campos)

        escritor.writeheader()
        for linha in leitor2:
            chave = linha[leitor2.fieldnames[0]]  # Usa a primeira coluna para encontrar a chave
            linha[label_col] = dados_arquivo1.get(chave, '')  # Busca a label correspondente, insere vazio se não encontrar
            escritor.writerow(linha)

    # Gerar estatísticas dos valores em "label"
    contador_labels = Counter(dados_arquivo1.values())
    estatisticas = dict(contador_labels)

    # Salvar as estatísticas em formato JSON
    with open(arquivo_saida+'.json', 'w', encoding='utf-8') as f_json:
        json.dump(estatisticas, f_json, ensure_ascii=False, indent=4)

# Substitua pelos nomes dos arquivos CSV
arquivo_csv1 = '../labeled_body_files.csv'  # Contém a coluna "label"
arquivo_csv2 = '/mnt/8811f502-ae19-4dd8-8371-f1915178f581/Fernando/DATASET/TESE/PER/PER2024-SOURCE/unlabeled_files.csv'
arquivo_csv_saida = 'labels_added.csv'

'''
Agrego os labels creados manualmente no body ao csv na coluna final do unlabel dataset com 3 colunas {body,face,skeleton}
'''
agregar_coluna_label(arquivo_csv1, arquivo_csv2, arquivo_csv_saida)

