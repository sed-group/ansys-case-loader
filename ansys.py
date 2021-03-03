import os
import argparse
import tempfile
import shutil
from pathlib import Path

# Parameters
job_dir_name = 'sed-job-ansys'
mechanical_var_file = 'mechanical'
geometry_var_file = 'geometry'
results_file = 'results.txt'

# Convenient variables
job_path = fr'{tempfile.gettempdir()}\{job_dir_name}'

parser = argparse.ArgumentParser(description='Run ANSYS simulation')
parser.add_argument('--journal', '-j', type=str, default="journal.wbjn", help='journal file path')
parser.add_argument('--mechanical', '-m', type=str, default="case.py", help='mechanical script file path')
parser.add_argument('--geometry', '-g', type=str, default="geometry.prt", help='Path to geometry')
parser.add_argument('--results', '-r', type=str, default="results/", help='Path to results directory.')
parser.add_argument('--name', type=str, default="ANSYS-EXPERIMENT", help='Name the experiment. Useful for identifying results later.')

args = parser.parse_args()

journal_file = args.journal
mechanical_file = args.mechanical
geometry_file = args.geometry
experiment_name = args.name
results_destination = args.results

# Check if job directory exists. Wipe it and create a new one.
if os.path.isdir(job_path):
    print(f'{job_path} exist. Wiping it.')
    shutil.rmtree(job_path)

# Create new job directory
os.mkdir(job_path)

# Create files with vars
f = open(fr'{job_path}\{geometry_var_file}', 'w')
f.write(geometry_file)
f.close()

f = open(fr'{job_path}\{mechanical_var_file}', 'w')
f.write(mechanical_file)
f.close()

# Prepare results file:
f = open(fr'{job_path}\{results_file}', 'w')
f.write(f'Name={experiment_name}\n')
f.close()

print('Turning over job to ANSYS workbench..')

os.system(f'RunWB2.exe -R {journal_file}')

# Offload results
if results_destination is not None:
    results_destination_file_path = fr'{results_destination}\{experiment_name}.txt'
    print(f'Storing results in {results_destination_file_path}')
    Path(results_destination).mkdir(parents=True, exist_ok=True)
    shutil.copyfile(fr'{job_path}\{results_file}', results_destination_file_path)

print('Done.')
