a=1
b=2
dicc = {a:1,b:2,3:3,4:4}
dicc[8]=8
print(dicc)

if 7 in dicc:
    print(dicc[7])
else:
    dicc[7]=7
print(dicc.get(6,"No existe la clave indicada"))
