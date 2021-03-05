# Prerequisites
- ANSYS
- Python 3.7 or newer
- ANSYS "RunWB2.exe" needs to be accessable through the PATH environment variable (for instannce "C:\Program Files\ANSYS Inc\v201\Framework\bin\Win64")

# Usage
If you are running this on a Windows machine, then the script needs to be run using cmd. Using git-bash (or similar) to run this script
may result in issues and strange ANSYS behaviour.

`python ansys.py --journal <JOURNAL_FILE_PATH> --geometry <GEOMETRY_FILE_PATH> --mechanical <MECHANICAL_SCRIPT_FILE_PATH> --name <NAME_OF_EXPERIMENT> --results <PATH_TO_RESULTS_DIRECTORY>`

You can use `python ansys.py --help` for more documentation. 

Here's an example:
`python ansys.py --journal case.wbjn --geometry "C:/Users/julianm/Documents/nx-models/generated_trs/hypercube/ns/trs_nsed.prt" --mechanical "C:\Users\julianm\Box\DIFAM - delad\ANSYS\case_script.py" --results "results/" --name "trs-experiment-01"`
