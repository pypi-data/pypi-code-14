import logging
import os
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

import tecplot
from tecplot.data.operate import execute_equation
from tecplot import active_frame

examples_dir = tecplot.session.tecplot_examples_directory()
infile = os.path.join(examples_dir, '3D', 'JetSurface.lay')
outfile = 'jet_surface.png'
tecplot.load_layout(infile)
current_dataset = active_frame().dataset  # type: tecplot.data.dataset.Dataset

# alter variable 'Nj' for the the two wing zones in the dataset
# In this simple example, just multiply it by 10.
execute_equation('{Nj}={Nj}*10', zones=[current_dataset.zone('right wing'),
                                        current_dataset.zone('left wing')])

# The contour color of the wings in the exported image will now be
# red, since we have altered the 'Nj' variable by multiplying it by 10.
tecplot.export_image(outfile)
