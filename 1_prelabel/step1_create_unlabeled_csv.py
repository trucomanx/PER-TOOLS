#!/usr/bin/python3

'''
Uma  vez ja creado os directorios com body, face e skel
    * listo de como path absoluto em png_files todos os arquivos png dentro de uma pasta chamada body.
    * verifica se os arquivos correspondentes de 'face' 
      (com a mesma base de nome) e 'skeleton' (com a extensão .npy) estão presentes no diretório esperado. 
      Os arquivos 'face'  e 'skeleton' são inferidos com base no local dos arquivos PNG.
    * Escreve um csv com os arquivos achados nas colunas body,face,skeleton sem label
      
Gere um CSV com os arquivos corretos e pareados para body, face e skeleton.
'''

INPUT_DIR   = '/mnt/8811f502-ae19-4dd8-8371-f1915178f581/Fernando/DATASET/TESE/PER/PER2024-SOURCE'
OUTPUT_DIR  = '/mnt/8811f502-ae19-4dd8-8371-f1915178f581/Fernando/DATASET/TESE/PER/PER2024-SOURCE'
OUTPUT_FILE = 'unlabeled_files.csv'

################################################################################

import os
import sys
#sys.path.append('../library') 

import SystemEmotion4Lib.tools_funcs as toolf


print('')
print('Working in directory:',INPUT_DIR)
png_files = toolf.list_png_in_match_subdir(INPUT_DIR,match_subdir='body',file_ext='.png');
print('Found',len(png_files),'png files in body directory')

print('')
print('Verifying',len(png_files),'png files.')
res, file_list = toolf.verify_dataset_body_structure(png_files);
print('Found',len(png_files),'png files')

print('')
if res:
    output_file=os.path.join(OUTPUT_DIR,OUTPUT_FILE);
    print("Achados",len(file_list),"arquivos válidos. Ver",output_file);
else:
    output_file=os.path.join(OUTPUT_DIR,'error_files.csv');
    print("Achados",len(file_list),"arquivos com defeito. Ver",output_file);
    
with open(output_file, 'w') as arquivo:
    arquivo.write('body,face,skeleton\n')
    for item in file_list:
        arquivo.write(  os.path.relpath(item[0],INPUT_DIR)+','+
                        os.path.relpath(item[1],INPUT_DIR)+','+
                        os.path.relpath(item[2],INPUT_DIR)+'\n')





