#Desempaque de tuplas e intercambio de variables
a,b,c = (1,2,3)

print(a)
print(b)
print(c)
print("---------------------------------------")
a,b=b,a

print(a)
print(b)
print("---------------------------------------")
#el asterisco(*) en una inicializacion de variable indica que la variable
#que la tenga recoge los valores  no asignados a las otras variables
a,b,c,*d,e,f,g=range(30)

print(a)
print(b)
print(c)
print(d)
print(e)
print(f)
print(g)
