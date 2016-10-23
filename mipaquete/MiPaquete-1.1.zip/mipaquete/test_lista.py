from math import sqrt as raiz
lista = [2,3,"Hola",[4,5]]#es opcional dejar una coma al final del ultimo elemento
print(lista)
print(lista[3][1])

cadena = "Hola Mundo"
print(cadena[5])


print(lista+lista)
print(lista*3)

lista[2]=[1,2,3]
print(lista)

if [1,2,3] in lista:
    print("Evaluar operador in: [1,2,3] esta en lista")

lista.append(6)
print("Se agrego un elemento a la lista con append: "+str(lista[4]))
print(lista)

print("Se inserto un elemento en la 1ra posicion")
lista.insert(0,1)
print(lista)

print("uso de index")
print("indice de 3 en la lista: "+str(lista.index(3)))

print("uso de max")
print("maximo elemento: "+str(max(lista[3])))

print("uso de min")
print("minimo elemento: "+str(min(lista[3])))

print("uso de count")
print("cantidad de veces que sale el 2 en la lista: "+str(lista.count(2)))

print("uso de remove")
print("se removio el 4 elemento: "+str(lista[3]))
lista.remove(lista[3])
print(lista)

print("uso de reverse")
lista.reverse()
print(lista)

print("uso de rango")
print("Se crea un objeto  con numeros de 3 a 30 con incrementos de 3:")
lista2=list(range(3,31,3))
print(lista2)

print("uso de for")
for i in lista2:
    print(i)


print("Cortes de lista:")
print("Lista:")
lista=list(range(0,100,3))
print(lista)
print(" Sublista. Desde el 3 hasta el 6to elemento:")
print(lista[2:6])
print(" Sublista. Desde el 5to elemento hasta el final:")
print(lista[4:])
print(" Sublista. Desde el 1ro hasta el 10mo elemento")
print(lista[:10])
print(" Sublista. Desde el 10mo elemento hasta el 30mo elemento, de tres en tres:")
print(lista[9:30:3])
print(" Sublista. Inversion de la lista usando [::-1] (Valido para strings):")
print(lista[::-1])
            

print("Listas por comprension:")
cubo = [i**2 for i in range(10) if i**2%2==0]
print(cubo)

print("Formateo de cadenas")
lista=[raiz(i) for i in range(1,100) if i%raiz(i) == 0]
print(lista)
cad = ""
for rt in lista:
    cad = cad+"Raiz de {0} = {1}".format(rt**2,rt)+". "
print(cad)

