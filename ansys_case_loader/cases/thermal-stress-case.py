# This script is for ANSYS Mechanical. It creates a simple thermal stress analysis.
# For future reference: Tree.GetPathToFirstActiveObject() is useful for figuring out references in Ansys Mechanical.
# Author: Julian Martinsson Bonde, julianm@chalmers.se

import tempfile

# Parameters
job_dir_name = 'sed-job-ansys'
results_file = 'results.txt'
deformation_points = 'deformation_points.txt'
stress_points = 'stress_points.txt'
