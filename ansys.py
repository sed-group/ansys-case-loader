# This script is used to start an ANSYS experiment from the command line.
# This will launch ANSYS and then run the specified workbench journal
# Author: Julian Martinsson, julianm@chalmers.se

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

verbose = False

# Convenient variables
job_path = fr'{tempfile.gettempdir()}\{job_dir_name}'


def run_case(journal_file, mechanical_file, geometry_file, experiment_name, results_destination):
    # Check if job directory exists. Wipe it and create a new one.
    if os.path.isdir(job_path):
        if verbose:
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

    if verbose:
        print('Turning over job to ANSYS workbench..')

    os.system(f'RunWB2.exe -R {journal_file}')

    # Offload results
    if results_destination is not None:
        results_destination_file_path = fr'{results_destination}\{experiment_name}.txt'

        if verbose:
            print(f'Storing results in {results_destination_file_path}')

        Path(results_destination).mkdir(parents=True, exist_ok=True)
        shutil.copyfile(fr'{job_path}\{results_file}', results_destination_file_path)

    if verbose:
        print('Done.')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run ANSYS simulation')
    parser.add_argument('--journal', '-j', type=str, default="journal.wbjn",
                        help='journal file path')
    parser.add_argument('--mechanical', '-m', type=str, default="case.py",
                        help='mechanical script file path')
    parser.add_argument('--geometry', '-g', type=str, default="geometry.prt",
                        help='Path to geometry')
    parser.add_argument('--results', '-r', type=str, default="results/",
                        help='Path to results directory.')
    parser.add_argument('--name', type=str, default="ANSYS-EXPERIMENT",
                        help='Name the experiment. Useful for identifying results later.')
    parser.add_argument('--verbose', '-v', action="store_true",
                        help='Spew out nonsense on stdout')

    args = parser.parse_args()
    verbose = args.verbose

    if verbose:
        print(f'Starting experiment {args.name}')

    run_case(args.journal, args.mechanical, args.geometry, args.name, args.results)
