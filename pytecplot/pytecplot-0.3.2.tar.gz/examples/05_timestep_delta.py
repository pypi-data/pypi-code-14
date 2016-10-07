"""
This script shows how to do the following:
    1) Open a layout file
    2) Use execute_equation() to calculate new variables which
       are the difference between two time steps
    3) Create a new frame and setup frame styles
    4) Export images for each time step.
"""
import tecplot as tp
from os import path

# Open the transient layout and acquire a handle to the dataset
examples_dir = tp.session.tecplot_examples_directory()
datafile = path.join(examples_dir, '2D', 'VortexShedding.lpk')
tp.load_layout(datafile)
dataset = tp.active_frame().dataset

def create_delta_variables(var_list):
    for v in var_list:
        equation = '{%s_Delta} = 0' % dataset.variable(v).name
        tp.data.operate.execute_equation(equation)

def calculate_delta(var_list, z1, z2):
    for v in var_list:
        var_num = v + 1
        equation = '{%s_Delta} = V%d - V%d[%d]' % (
            dataset.variable(v).name, var_num, var_num, z1.index + 1)
        tp.data.operate.execute_equation(equation, zones=[z2])

variable_list = range(2, dataset.num_variables)
create_delta_variables(variable_list)

# Now we actually calculate the delta between two zones at different time steps.
for z in range(0, dataset.num_zones-1):
    calculate_delta(variable_list, dataset.zone(z), dataset.zone(z+1))

# Get a handle to the current frame and create a new frame
frame1 = tp.active_frame()
frame2 = tp.active_page().add_frame()
frame2.plot_type = tp.constant.PlotType.Cartesian2D

# Ensure frame1 is activated before setting its style.
# In future versions of PyTecplot
# there will by Python APIs which replace the tp.macro.execute_command() calls
frame1.activate()
tp.macro.execute_command("""$!SETCONTOURVAR
  VAR = %d
  CONTOURGROUP = 1
  LEVELINITMODE = RESETTONICE""" %(dataset.variable("P(N/M2)").index+1))
tp.macro.execute_command("""
$!FIELDLAYERS SHOWCONTOUR = TRUE
$!LINKING BETWEENFRAMES{LINKSOLUTIONTIME = YES}
$!LINKING BETWEENFRAMES{LINKXAXISRANGE = YES}
$!LINKING BETWEENFRAMES{LINKYAXISRANGE = YES}
$!PROPAGATELINKING
  LINKTYPE = BETWEENFRAMES
  FRAMECOLLECTION = ALL""")

# Ensure frame2 is active before setting its style
frame2.activate()
tp.macro.execute_command("""$!SETCONTOURVAR
  VAR = %d
  CONTOURGROUP = 1
  LEVELINITMODE = RESETTONICE""" % (dataset.variable("P(N/M2)_Delta").index+1))

tp.macro.execute_command("$!FIELDLAYERS SHOWCONTOUR = TRUE "
                         "$!CONTOURLEVELS RESET NUMVALUES = 11 "
                         "CONTOURGROUP = 1 $!GLOBALCONTOUR 1 "
                         "COLORMAPNAME = 'Diverging - Blue/Red'")

# Collect the solution times in this dataset
times = set()
for z in dataset.zones():
    times.add(z.solution_time)

# Iterate over the solution times and export an image for each solution time.
# Note that frame2 is still the active frame
# and is the one that will be exported.
frame2.activate()
for t in sorted(times)[1:4]:
    tp.macro.execute_command("$!GLOBALTIME SOLUTIONTIME = %f" % t)
    tp.export_image(r'timestepdelta_%f.png' % t)
