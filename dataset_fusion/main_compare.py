#!/usr/bin/python3

import pandas as pd

def comparar_csvs(arquivo1, arquivo2, roundval=3):
    # Carregar os arquivos CSV em DataFrames
    df1 = pd.read_csv(arquivo1)
    df2 = pd.read_csv(arquivo2)

    # Arredondar todos os números para 3 casas decimais
    df1 = df1.round(roundval)
    df2 = df2.round(roundval)

    # Comparar se os DataFrames são iguais
    if df1.equals(df2):
        print("✅ Os arquivos são IGUAIS após arredondamento.")
    else:
        print("❌ Os arquivos são DIFERENTES após arredondamento.")

        # Exibir as diferenças
        diff = df1.compare(df2)
        print("\nDiferenças encontradas:")
        print(diff)

# Exemplo de uso

print("\n\nncod81_efficientnet_b3_efficientnet_b3_minus/test.csv")
file1="full2024-fusion/ncod81_efficientnet_b3_efficientnet_b3_minus/test.csv"
file2="../../../full2024-fusion/ncod81_efficientnet_b3_efficientnet_b3_minus/test.csv"
comparar_csvs(file1,file2, roundval=3) ## file1 == self  ## file2 == other 

print("\n\nncod81_efficientnet_b3_efficientnet_b3_minus/train.csv")
file1="full2024-fusion/ncod81_efficientnet_b3_efficientnet_b3_minus/train.csv"
file2="../../../full2024-fusion/ncod81_efficientnet_b3_efficientnet_b3_minus/train.csv"
comparar_csvs(file1,file2, roundval=3) ## file1 == self  ## file2 == other 


print("\n\nncod81_efficientnet_b3_efficientnet_b3/test.csv")
file1="full2024-fusion/ncod81_efficientnet_b3_efficientnet_b3/test.csv"
file2="../../../full2024-fusion/ncod81_efficientnet_b3_efficientnet_b3/test.csv"
comparar_csvs(file1,file2, roundval=4) ## file1 == self  ## file2 == other 

print("\n\nncod81_efficientnet_b3_efficientnet_b3/train.csv")
file1="full2024-fusion/ncod81_efficientnet_b3_efficientnet_b3/train.csv"
file2="../../../full2024-fusion/ncod81_efficientnet_b3_efficientnet_b3/train.csv"
comparar_csvs(file1,file2, roundval=4) ## file1 == self  ## file2 == other 
