# This script is for ANSYS Mechanical. It creates a simple static structural analysis.
# For future reference: Tree.GetPathToFirstActiveObject() is useful for figuring out references in Ansys Mechanical.
# Author: Julian Martinsson

import tempfile

# Parameters
job_dir_name = 'sed-job-ansys'
results_file = 'results.txt'

element_size = 10   # [mm]
pinch_tol = 4       # [mm]
force_y = 3000      # N
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
analysis_list = DataModel.AnalysisList[0]

# Apply a force
force = analysis_list.AddForce()
force.Location = DataModel.GetObjectsByName("NS_cone_flange")[0]
force.DefineBy = LoadDefineBy.Components
force.YComponent.Output.SetDiscreteValue(0, Quantity(force_y, "N"))

# Apply a fixed support
fixed_support = analysis_list.AddFixedSupport()
fixed_support.Location = DataModel.GetObjectsByName("NS_outer_flange")[0]

# Add requested measurements
analysis_list.Solution.AddTotalDeformation()
analysis_list.Solution.AddEquivalentStress()

# Solve 
analysis_list.Solve()

# Extract results
max_deform = Model.Analyses[0].Solution.Children[1].Maximum      # Maximum deformation
max_stress = Model.Analyses[0].Solution.Children[2].Maximum      # Maximum stress

f = open(job_path + '\\' + results_file, 'a')
f.write('max_deformation='+str(max_deform)+'\n')
f.write('max_stress='+str(max_stress)+'\n')