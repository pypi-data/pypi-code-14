import commands

from vaspy.matstudio import XsdFile

filename = (status, output) = commands.getstatusoutput('ls *.xsd | head -1')
xsd = XsdFile(filename=filename)
poscar_content = xsd.get_poscar_content(bases_const=1.0)
with open('POSCAR', 'w') as f:
    f.write(poscar_content)
