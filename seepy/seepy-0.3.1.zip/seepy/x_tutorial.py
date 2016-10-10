#! #*SeePy tutorial*

#%img x_monty.png

#!
'''
Please look at SeePy report window and your tutorial *.py file editor that has just run.
Please try change the scrip in editor and use save<Ctrl+s> to see how report is changing.
But first check does watch script option in toolbar is active.
'''

#! ------------------------------------------------------------

#! Let's write some python script to calculate something.

a = 12
b = 25
c = a + b
print a

#!
'''
You can run this script as normal *.py script - run it by <F5> in script editor.
You have seen the `a` value in shell output. But you can see it in your SeePy report ...
'''

a #! - here it is

#! Let's change a value 

a = 30 #! - here is changed value


#! ------------------------------------------------------------

#!
'''
You can call variable values in this comments.
So, we have %(a)s , %(b)s and %(c)s.

And the other way is val_a and var_a
'''

#! ------------------------------------------------------------

#!
'''
You can still run this script as
normal *.py script - run it by <F5> in script editor.
As you can guess python engine does't see the SeePy syntax.
'''

#! ------------------------------------------------------------

#!
'''
SeePy comments use Markdown.

#Title
##Title
###Title

*some text*

**some text**

* Title
* Title2

More about Markdown you can see here
https://daringfireball.net/projects/markdown/

Here is Markdown tutorial
http://www.markdowntutorial.com/
'''

#! ------------------------------------------------------------

#! You can see python code from your script in SeePy report

#%code
r = 120
import math
math.pi
area = math.pi * r ** 2
#%

#! for one line code

area = math.pi * r ** 2 #%code


area #!- here is what we get

#! ------------------------------------------------------------

#! Go to Script>Float precission in menu to change float precision.

#! ------------------------------------------------------------

#!
'''
Lets show image in your report,
the image file must be storef in the same directory where you script is.
'''

#%img x_python.png

#! ... here our Python is.

#! ------------------------------------------------------------

#! What about plotting?? You can use Matplotlib pyplot - here is some example

import matplotlib.pyplot as plt
import numpy as np
t = np.arange(-1.0, 2.0, 0.01)
s1 = np.cos(9*np.pi*t) + 3 * t ** 2
plt.plot(t, s1)
plt #%plt
plt.clf()

#! ------------------------------------------------------------

#! If you need to publish some mathematical formula LaTex syntax can be used

#! You can write some LaTex as comment
#%tex s(t) = \mathcal{A}\mathrm{sin}(2 \omega t)

#! or if the LaTex fomula is in you python code
pi = 3.14
r = 40
Area = pi * r ** 2 #%tex

#! or if the LaTex fomula is defined as python string
LaTexString = '\lim_{x \to \infty} \exp(-x) = 0'
LaTexString #%stringtex

#! ------------------------------------------------------------

#!
'''
You can change python variables in report, so finally you don't need to edit
script source to change input data. Please not that the new values will
be stored in the script source.
'''

a = 120 #! - this is not interactive variable in your report
b = 66 #<< - this is interactive variable in your report - click to change it
#! Those values are var_a and var_b.

#! Other display effects are possible
b = 66 #<< your comment
b = 66 #<<< your comment
b = 66 #<<<< your comment

#! If your variable is equal some list element, you can select list element interactively:
somelist = [1, 2, 3, 4]
variable = somelist[2] #<< - select variable value

#! or with othet display effects
variable = somelist[2] #<< - select variable value
variable = somelist[1] #<<< - select variable value
variable = somelist[1] #<<<< select variable value

#! *Examples of use*

#! *Example 1*
car_list = ['volvo', 'toyota', 'saab', 'fiat']
your_car = car_list[0] #<<< - select your car
#! Your car is %(your_car)s.

#! *Example 2*
material_list = ['steel', 'concrete', 'plastic', 'wood']
material = material_list[0] #<<<< Material is - 
#! The %(material)s will be used to make something.

#! *Example 3*
temperature_range = range(10,30,1)
room_temperature = temperature_range[17] #<<<< Select the room temperature - 
#! Temperature %(room_temperature)s Celsius degree selected.

#! ------------------------------------------------------------

#! What about drawing in report ?? You can create drawing using SVG syntax.

#! Python string with SVG syntax can be rendered.

svgsyntax='''
<svg height="55" width="55">
    <circle cx="30" cy="30" r="20"
    stroke="black" stroke-width="1" fill="tan" /> 
</svg>
'''
svgsyntax #%svg

#! so this is the way to get parametric drawing

r = 50 #<< - circle radius value
xs = 120 #<< - center x
ys = 70 #<< - center y
svgsyntax='''
<svg height="150" width="200">
    <circle cx="{1}" cy="{2}"
    r="{0}" stroke="black" stroke-width="1" fill="tan" />
    <text x="{1}" y="{2}" fill="black"
    font-size="15">circle {0} radius </text>  
</svg>
'''.format(r, xs, ys)
#! for this parameters we have
svgsyntax #%svg

#!To make parametrise easer you can use `svgwrite` package

import svgwrite
a = 60 #<< - rec a dimension
b = 100 #<< - rec b dimension
svg_document = svgwrite.Drawing(size = (200, 100))
svg_document.add(svg_document.rect(insert = (0, 0), size = (a, b),
                                   stroke_width = "1",stroke = "black",fill = "tan"))
svg_document.add(svg_document.text("Rectangle size" + str(a)+ 'x' +str(b) ,
                                   insert = (a/2-20, b/2)))
svg_document #%svg 

#! ------------------------------------------------------------

#! Mathematical expressions and equations
#! You can add to SeePy report expressions and equations with optional comment 
a = 1
b = 3
c = 3*a + 4*b #%requ - your comment
c = 3*a + 4*b #%requ
c = 3*a + 4*b #%equ - your comment
c = 3*a + 4*b #%equ
3*a + 4*b #%requ - your comment
3*a + 4*b #%requ
3*a + 4*b #%equ - your comment
3*a + 4*b #%equ

#! Python code is format to look more natural

import math
math.pi #%equ
math.sin(1) #%equ
2**2 #%equ

#! When you working with SI units using Unum package

from unum import units as u
5 * u.m + 10 * u.mm #%requ
(5 * u.m + 10 * u.mm).asUnit(u.km) #%requ

#! ------------------------------------------------------------

#! ##Go to Info>Syntax help to get know abaut all available  SeePy syntax.


