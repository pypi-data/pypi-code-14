from pyibex import *
import numpy as np
from vibes import vibes




# init drawing area
vibes.beginDrawing()
vibes.newFigure('Result')
vibes.setFigureProperties({'x': 0, 'y': 0, 'width': 1000, 'height': 1000})

#configure pySIVIA output
params = {'color_in': '#888888[#444444]', 'color_out':
          '#888888[#DDDDDD]', 'color_maybe': '#888888[q]', 'use_patch' : True}

# create the initial box X0 = [-10, 10] x [-10, 10]
X0 = IntervalVector(3, [-4, 4])  # '#888888[#DDDDDD]'
X0 = IntervalVector(2, [-4, 4])  # '#888888[#DDDDDD]'

f = Function("x", "y", "z", "x^2+y^2+z^2")
sep = SepProj(SepFwdBwd(f, Interval(0, 1)), IntervalVector(1, [0.5, 1]), 0.001)
# sep = SepFwdBwd(f, Interval(0, 4))
# run SIVIA
(res_in, res_out, res_y) = pySIVIA(X0, sep, 0.01)


# vibes.drawAUV(robot[0], robot[1], 1, np.rad2deg(0.3))
# for (x, y), d in zip(landmarks, dist):
#     vibes.drawCircle(x,y, 0.1, "[k]")
#     vibes.drawCircle(x,y, d.lb(), "k")
#     vibes.drawCircle(x,y, d.ub(), "k")

#equalize axis lenght
vibes.axisEqual()


vibes.endDrawing()
