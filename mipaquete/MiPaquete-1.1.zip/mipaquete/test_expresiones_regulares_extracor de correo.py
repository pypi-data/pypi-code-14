import re
patron=r"([\w\.\-_]+)@([\w\.\-_]+)(\.[\w\.]+)"
cadena = "Llamar a julio_munoz@evalueserve.com para mayor informacion, correo personal julioc.munozg@gmail.com juliocmg-88@yahoo.es"

p = re.compile(patron)
for correo  in p.finditer(cadena):
    print(correo.group())
