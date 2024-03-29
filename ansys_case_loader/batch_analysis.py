# This script is used to start a batch of ANSYS experiments from the command line (or as a module).
# This will launch ANSYS and then run the specified workbench journal
# Author: Julian Martinsson Bonde, julianm@chalmers.se

from ansys_case_loader.ansys import run_case
from ansys_case_loader.results_parser import parse_results_dir

import argparse
import os


def batch_run(geometry_directory, journal, mechanical_script, results_directory,
              verbose=False,
              skip_completed=True,
              csv: bool = False):
    geometry_directory = os.fsencode(geometry_directory)
    if os.path.isdir(geometry_directory) is False:
        raise ValueError(f'Geometry directory {geometry_directory} does not exist.')

    for file in os.listdir(geometry_directory):
        filename = os.fsdecode(file)
        filename_no_ext = os.path.splitext(filename)[0]
        file_path = os.fsdecode(geometry_directory) + '/' + filename
        # Only treat NX CAD files
        if filename.endswith('.prt') is False:
            continue

        run_name = filename_no_ext

        if os.path.isfile(results_directory + '/' + filename_no_ext + '.xd') and skip_completed:
            if verbose:
                print(f'{filename} has already been processed. Skip.')
            continue

        run_case(journal, mechanical_script, file_path, run_name, results_directory, verbose=verbose)

    if csv:
        parse_results_dir(results_directory, output=f'{results_directory}/results.csv')


if __name__ == "__main__":
    # Get location of this script to locate default cases and journals
    script_path = os.path.realpath(__file__)
    script_dir_path = os.path.dirname(script_path)

    parser = argparse.ArgumentParser(description='Run ANSYS simulation in batch')
    parser.add_argument('--geodir', '-gd', type=str, default='geometry/',
                        help='Directory with CAD files for analysis')
    parser.add_argument('--mechanical', '-m', type=str, default=f"{script_dir_path}/cases/case.py",
                        help='mechanical script file path')
    parser.add_argument('--results', '-r', type=str, default=f"{script_dir_path}/../results/",
                        help='Path to results directory.')
    parser.add_argument('--journal', '-j', type=str, default=f"{script_dir_path}/wb_journals/journal.wbjn",
                        help='journal file path')
    parser.add_argument('--verbose', '-v', action="store_true",
                        help='Spew out nonsense on stdout for your entertainment')
    parser.add_argument('--compile-results', '-cr', action="store_true", default=True,
                        help='Compile results into a neat csv document')

    args = parser.parse_args()

    if args.verbose:
        print('Initiating batch run.')

    make_csv = False
    if args.compile_results:
        make_csv = True

    batch_run(args.geodir, args.journal, args.mechanical, args.results, verbose=args.verbose, csv=make_csv)
