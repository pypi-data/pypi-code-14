import ezdxf

dwg = ezdxf.readfile('flags.dxf')

for e in dwg.entities:
    print(e.dxftype())