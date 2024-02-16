# This script is for ANSYS Mechanical. It creates a simple thermal stress analysis.
# For future reference: Tree.GetPathToFirstActiveObject() is useful for figuring out references in Ansys Mechanical.
# Author: Julian Martinsson Bonde, julianm@chalmers.se

import tempfile

# Parameters
job_dir_name = 'sed-job-ansys'
results_file = 'results.txt'
deformation_points = 'deformation_points.txt'
stress_points = 'stress_points.txt'

element_size = 10   # [mm]
pinch_tol = 4       # [mm]
onset_vane_temperature = 650    # deg C
onset_outside_temperature = 20  # deg C
material_name = "Inconel 718"   # The specified material needs to be present in the template

# Convenient variables
job_path = tempfile.gettempdir() + '\\' + job_dir_name

# Create a mesh
mesh = DataModel.Project.Model.Mesh

sizing = mesh.AddSizing()
sizing.Location = DataModel.GetObjectsByName("NS_body")[0]  # NS_body is a Named Selection imported from Siemens NX
sizing.ElementSize = Quantity(element_size, "mm")
mesh.PinchTolerance =  Quantity(pinch_tol, "mm")

mesh.Update()

# Apply material
material = None
for m in Model.Materials.Children:
    if material_name in m.Name:
        material = m

material_assignment = Model.Materials.AddMaterialAssignment()
material_assignment.Location = DataModel.GetObjectsByName("NS_body")[0]
material_assignment.Material = material.Name

# Create a new analysis
thermal_analysis = DataModel.AnalysisList[0]
structural_analysis = DataModel.AnalysisList[1]

# Apply temperature to vanes
vane_temp = thermal_analysis.AddTemperature()
vane_temp.Location =  DataModel.GetObjectsByName("NS_vane_surface")[0]
vane_temp.Magnitude.Output.SetDiscreteValue(0, Quantity(onset_vane_temperature, "C"))

# Apply temperature to outer case
outer_temp = thermal_analysis.AddTemperature()
outer_temp.Location = DataModel.GetObjectsByName("NS_outer_outside_surface")[0]
outer_temp.Magnitude.Output.SetDiscreteValue(0, Quantity(onset_outside_temperature, "C"))

# Apply a fixed support
fixed_support = structural_analysis.AddFixedSupport()
fixed_support.Location = DataModel.GetObjectsByName("NS_outer_flange")[0]

# Add requested measurements
thermal_analysis.Solution.AddTemperature()
structural_analysis.Solution.AddTotalDeformation()
structural_analysis.Solution.AddEquivalentStress()

# Solve 
structural_analysis.Solve()

# Extract results
temperature_solution = thermal_analysis.Solution.Children[1]      # Maximum deformation
deformation_solution = structural_analysis.Solution.Children[1]      # Maximum stress
equivalent_stress_principal_solution = structural_analysis.Solution.Children[2]  # Max Principal stress

# Get result variables
th_max_deformation = deformation_solution.Maximum
th_max_principal_stress = equivalent_stress_principal_solution.Maximum

# Write results file
f = open(job_path + '\\' + results_file, 'a')
f.write('th_max_deformation='+str(th_max_deformation)+'\n')
f.write('th_max_stress='+str(th_max_principal_stress)+'\n')
f.close()
