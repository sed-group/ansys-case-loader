# Prerequisites
- ANSYS
- Python 3.7 or newer
- ANSYS "RunWB2.exe" needs to be accessable through the PATH environment variable (for instance "C:\Program Files\ANSYS Inc\v201\Framework\bin\Win64")

# Usage
To run either single or batch mode, you need to have a certain amount of memory allocated to the process. 
However, the import structure of this project can be a bit messy. There are (at least) two ways of using this code:
1) Run the program directly from cmd.exe. This can be a bit tricky, 
as you will need to adjust the python path according to the errors you will undoubtedly receive.
2) Run the program using PyCharm. This it, in my opinion, __the easiest option__, 
as you can configure your pypath directly in your launch configuration. However, this code requires a substantial 
amount of memory in order to properly run ANSYS. By default, PyCharm allocated too little memory. To fix this, 
open the repo in PyCharm as a pycharm project, and find the Help menu at the top. 
From there, navigate to "Change Memory Settings". Here, I use 14000MiB. You could of course do even higher 
if you have the capacity. However, lower values risk resulting in crashes which will ruin the results.

When running the case, either using cmd.exe or pycharm (or some other IDE), you will need to give the script 
a set or parameters. There are some examples below. You can use `python ansys.py --help` for more documentation. 

## Single analysis
`ansys.py --journal <JOURNAL_FILE_PATH> --geometry <GEOMETRY_FILE_PATH> --mechanical <MECHANICAL_SCRIPT_FILE_PATH> --name <NAME_OF_EXPERIMENT> --results <PATH_TO_RESULTS_DIRECTORY>`

Here's an example:
`python ansys.py --journal case.wbjn --geometry "C:/Users/julianm/Documents/nx-models/generated_trs/hypercube/ns/trs_nsed.prt" --mechanical "C:\Users\julianm\Documents\ANSYS\case_script.py" --results "results/" --name "trs-experiment-01"`

## Batch analysis
`batch_analysis.py -gd <DIRECTORY_WITH_CADFILES_> -m "ansys_case_loader\cases\linear-buckling-case.py" -j "ansys_case_loader\wb_journals\linear-buckling.wbjn" --verbose`



