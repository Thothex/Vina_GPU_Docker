import subprocess
import os
import sys
import pandas as pd 
import time
import re
from tqdm import tqdm

# SELECT PROTEIN
protein = '4j1r'

path_ligand_dir = os.path.join(os.getcwd(), 'ligands')
path_ligand_dir_docked = os.path.join(os.getcwd(), 'docked_data_tables', f'{protein}')
path_original_config = os.path.join(os.getcwd(), 'proteins', f'{protein}_protein_config.txt')
path_dataset_smiles_ligand = os.path.join(os.getcwd(), 'smiles_ligands_data.csv')

def parse_ligand_file(file_path):
    ligand_data = {}
    current_ligand = None
    min_energy = None

    with open(file_path, 'r') as file:
        for line in file:
            if "Refining ligand" in line:
                if current_ligand and min_energy is not None:
                    ligand_data[current_ligand] = min_energy
                ligand_match = re.search(r'ligand_\d+', line)
                if ligand_match:
                    current_ligand = ligand_match.group()
                    min_energy = None 
            
            if re.match(r'\s*1\s+', line) and current_ligand:
                try:
                    min_energy = float(line.split()[1]) 
                except (IndexError, ValueError):
                    continue
        if current_ligand and min_energy is not None:
            ligand_data[current_ligand] = min_energy
    return pd.DataFrame(list(ligand_data.items()), columns=['Ligand', 'Minimum Energy'])


if not os.path.exists(path_ligand_dir_docked):
    os.makedirs(path_ligand_dir_docked, exist_ok=True)
    fragments = {}
else:
    fragments = {csv.split('.csv')[0].split('_')[-1] for csv in os.listdir(path_ligand_dir_docked)}

dirs = os.listdir(path_ligand_dir)
dirs = [dir for dir in dirs if '_out' not in dir]
docked_parts = {dir for dir in dirs if dir.split('_')[-1] in fragments}

selected_parts = set(dirs) - docked_parts
smiles_ligand_dataframe = pd.read_csv(path_dataset_smiles_ligand)
smiles_ligand_dataframe['Ligand'] = smiles_ligand_dataframe['Ligand'].astype(str)
for dir in tqdm(selected_parts):
    print(f'Start calculation for %s' % dir)
    start = time.time()
    ligands = []
    energy = []
    smiles_list = []

    with open(path_original_config, 'r', encoding='utf-8') as file:
        content = file.read()
        modified_content = content.replace('ligand_directory = ./test_2', f'ligand_directory = ./ligands/{dir}')
        modified_content = modified_content.replace('opencl_binary_path = ./Vina-GPU-2.1/QuickVina2-GPU-2.1', f'opencl_binary_path = {os.getcwd()}')
        new_path = os.path.join(path_ligand_dir, dir, 'config.txt')
    with open(new_path, 'w', encoding='utf-8') as new_file:
        new_file.write(modified_content) 

    path_tmp_file = os.path.join(os.getcwd(), 'ligands', f'{dir}', 'result.txt')
    cmd = f'./QuickVina2-GPU-2-1 --config ./ligands/{dir}/config.txt > ./ligands/{dir}/result.txt'
    process = subprocess.Popen(cmd, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    process.wait()

    part_df = parse_ligand_file(path_tmp_file)
    os.remove(path_tmp_file)
    part_df['Ligand'] = part_df['Ligand'].astype(str)   
    result_df = pd.merge(part_df, smiles_ligand_dataframe, on='Ligand', how='left')

    result_df.to_csv(os.path.join(path_ligand_dir_docked, f'docked_{protein}_{dir}.csv'))
    end = time.time()
    # ОТПРАВКА НА БАКЕТ 
    print(f'{dir.upper()} calculated and saved! It took {end-start} seconds')








