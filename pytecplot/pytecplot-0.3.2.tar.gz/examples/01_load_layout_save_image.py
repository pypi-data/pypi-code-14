import logging
import os
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

import tecplot

examples_dir = tecplot.session.tecplot_examples_directory()
infile = os.path.join(examples_dir, '3D', 'JetSurface.lay')
outfile = 'jet_surface.png'
tecplot.load_layout(infile)
tecplot.export_image(outfile)
