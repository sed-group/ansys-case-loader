# This script is for ANSYS Mechanical. It creates a simple static structural analysis.
# For future reference: Tree.GetPathToFirstActiveObject() is useful for figuring out references in Ansys Mechanical.
# Author: Julian Martinsson, julianm@chalmers.se

import tempfile

# Parameters
job_dir_name = 'sed-job-ansys'
results_file = 'results.txt'
deformation_points = 'deformation_points.txt'
stress_points = 'stress_points.txt'

element_size = 10   # [mm]      Finite Element size.
pinch_tol = 4       # [mm]      Seems to increase script robustness slightly
force_y = 3000      # N         Force applied to flange
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

# Setup analysis
ss_analysis = DataModel.AnalysisList[0]     # Static structural analysis
eb_analysis = DataModel.AnalysisList[1]     # Eigenvalue Buckling analysis

# Apply a force
force = ss_analysis.AddForce()
force.Location = DataModel.GetObjectsByName("NS_cone_flange")[0]
force.DefineBy = LoadDefineBy.Components
force.YComponent.Output.SetDiscreteValue(0, Quantity(force_y, "N"))

# Apply a fixed support
fixed_support = ss_analysis.AddFixedSupport()
fixed_support.Location = DataModel.GetObjectsByName("NS_outer_flange")[0]

# Add requested measurements
ss_analysis.Solution.AddTotalDeformation()
ss_analysis.Solution.AddEquivalentStress()
eb_analysis.Solution.AddTotalDeformation()

# Solve
ss_analysis.Solve()
eb_analysis.Solve()

# Extract results
ss_total_deformation = Model.Analyses[0].Solution.Children[1]    # Maximum deformation
ss_equivalent_stress = Model.Analyses[0].Solution.Children[2]    # Maximum stress
eb_deform_solution = Model.Analyses[1].Solution.Children[1]     # Buckling total deformation

# Export results
ss_max_deform = ss_total_deformation.Maximum      # Maximum deformation
ss_max_stress = ss_equivalent_stress.Maximum      # Maximum stress
eb_load_multiplier = eb_deform_solution.LoadMultiplier

ss_total_deformation.ExportToTextFile(job_path + '\\' + deformation_points)
ss_equivalent_stress.ExportToTextFile(job_path + '\\' + stress_points)

# Write results file
f = open(job_path + '\\' + results_file, 'a')
f.write('ss_max_deformation='+str(ss_max_deform)+'\n')
f.write('ss_max_stress='+str(ss_max_stress)+'\n')
f.write('eb_load_multiplier='+str(eb_load_multiplier)+'\n')
f.close()
