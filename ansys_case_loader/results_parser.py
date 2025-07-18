# This script is used to parse the results generated from the analysis
# Author: Julian Martinsson Bonde, julianm@chalmers.se

import re
import argparse
import os
import datetime as dt


def find_parameter(content, parameter_name, value_type: str = 'number'):
    # Regex explanation:
    # Group 1 = parameter name                  (max_deformation=)
    # Group 2 = value, with or without decimal  (\d+\.?\d+))
    # Group 3 = Optional unit capture group
    # Group 4 = unit                            \s\[(.+)\]\n
    re_results = None
    if str.lower(value_type) == 'number':
        re_results = re.search(rf'({parameter_name})=(-?\d+\.?\d+)(\s\[(.+)\])?\n', content, re.IGNORECASE)
    elif str.lower(value_type) == 'string':
        re_results = re.search(rf'({parameter_name})=(.+)\n', content, re.IGNORECASE)

    value = None
    if re_results:
        value = re_results.group(2)

    return value


def parse_results_file(path, csv_target):
    f = open(path, 'r')
    content = f.read()
    f.close()

    # This is stupid and should be generalized but I am too lazy
    date_str = dt.datetime.fromtimestamp(os.path.getmtime(path)).strftime("%d/%m/%Y %H:%M:%S")
    experiment_name = find_parameter(content, 'name', 'string')
    max_deformation = find_parameter(content, 'ss_max_deformation', 'string')
    max_stress = find_parameter(content, 'ss_max_stress', 'number')
    buckling_load_multiplier = find_parameter(content, 'eb_load_multiplier', 'number')
    th_max_deformation = find_parameter(content, 'th_max_deformation')
    th_max_stress = find_parameter(content, 'th_max_stress')

    if max_deformation:
        print(f'{experiment_name}\tmax_deformation = {max_deformation}')
    else:
        print(f'No value for {path}')

    # If the file is new, then create a spreadsheet header
    if os.path.exists(csv_target) is False:
        f = open(csv_target, 'w')
        f.write(f'Date\tExperiment Name\tMax Deformation\tMax Stress\tBuckling Load Multiplier\tThermal deformation\tThermal stress\n')

    f = open(csv_target, 'a')
    f.write(f'{date_str}\t{experiment_name}\t{max_deformation}\t{max_stress}\t{buckling_load_multiplier}\t{th_max_deformation}\t{th_max_stress}\n')
    f.close()


def parse_results_dir(path, output='results/results.csv'):

    # Loop over files in dir
    directory = os.fsencode(path)

    print(f'Results directory contains {len(os.listdir(directory))} files.')

    for file in os.listdir(directory):
        filename = os.fsdecode(file)

        if filename.endswith(".xd") is False:
            continue

        file_path = fr'{path}\{filename}'
        parse_results_file(file_path, csv_target=output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run ANSYS simulation in batch')
    parser.add_argument('--resdir', '-rd', type=str, default='results/',
                        help='Directory with results files that you wish to parse')
    parser.add_argument('--output', '-o',
                        help='Output file')
    parser.add_argument('--verbose', '-v', action="store_true",
                        help='Spew out nonsense on stdout for your entertainment')

    args = parser.parse_args()

    if args.verbose:
        print('Initiating results parser.')

    if args.output is not None:
        parse_results_dir(args.resdir, args.output)
    else:
        parse_results_dir(args.resdir)
