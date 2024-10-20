import subprocess
import os
import sys
import pandas as pd 
import time
import re
import boto3
from botocore.config import Config

def upload_file_obj_to_s3(obj, s3_uri, s3=create_s3_session()):
    s3.upload_fileobj(obj, 'sber-projects', s3_uri)

# поменять пути
path_ligand_dir = '/Vina-GPU-2.1/QuickVina2-GPU-2.1/ligands'
path_ligand_dir_docked = '/Vina-GPU-2.1/QuickVina2-GPU-2.1/docked_data_tables'
path_original_config = '/Vina-GPU-2.1/QuickVina2-GPU-2.1/input_file_example/4j1r_protein_config.txt'
path_dataset_smiles_ligand = '/Vina-GPU-2.1/QuickVina2-GPU-2.1/smiles_ligands_data.csv'

if not os.path.exists(path_ligand_dir_docked):
    os.makedirs(path_ligand_dir_docked)
    fragments = {}
else:
    fragments = {csv.split('.csv')[0].split('_')[-1] for csv in os.listdir(path_ligand_dir_docked)}
dirs = os.listdir(path_ligand_dir)
dirs =  [dir for dir in dirs if '_out' not in dir]

docked_parts = {dir for dir in dirs if dir.split('_')[-1] in fragments}

selected_parts = set(dirs) - docked_parts
smiles_ligand_dataframe = pd.read_csv(path_dataset_smiles_ligand)
smiles_ligand_dataframe['Ligand'] = smiles_ligand_dataframe['Ligand'].astype(str)

for dir in selected_parts:
    ligands = []
    energy = []
    smiles_list = []

    with open(path_original_config, 'r', encoding='utf-8') as file:
        content = file.read()
    modified_content = content.replace('ligand_directory = ./test_2', f'ligand_directory = ./ligands/{dir}')
    new_path = os.path.join(path_ligand_dir, dir, 'config.txt')
    with open(new_path, 'w', encoding='utf-8') as new_file:
        new_file.write(modified_content) 

    cmd = f'./QuickVina2-GPU-2-1 --config ./ligands/{dir}/config.txt'

    process = subprocess.Popen(cmd, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output_lines = []
    for line in process.stdout.readlines():
        print(line)
        if line == '' and process.poll() is not None:
            break
        if line:
            output_lines.append(line.strip())

    data = []
    current_ligand = None

    for text in output_lines:
        if current_ligand is None:
            ligand_match = re.search(r'^Refining ligand .+/ligand_(\d+)', text)
            if ligand_match:
                current_ligand = ligand_match.group(1)

        affinity = re.search(r'^1\s+(-?\d+\.\d+)', text, re.MULTILINE)
        if affinity:
            affinity_value = affinity.group(1)
            if current_ligand:
                ligands.append(f'ligand_{current_ligand}')
                energy.append(affinity_value)
            current_ligand = None

        df = pd.DataFrame([ligands, energy]).transpose()
        df.columns=['Ligand', 'Energy']
    df['Ligand'] = df['Ligand'].astype(str)   
    result_df = pd.merge(df, smiles_ligand_dataframe, on='Ligand', how='left')
    result_df.to_csv(os.path.join(path_ligand_dir_docked, f'docked_4j1r_protein_new_{dir}.csv'))
    upload_file_obj_to_s3(result_df, f'docked_4j1r_protein_new_{dir}.csv')
    print(f'READY {dir}!!!')








