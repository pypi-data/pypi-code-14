from random import randint as azar
from math import pi
print("Funciones de cadenas:")
lista=[str(i) for i in range(10)]
print("join: convierte elementos de una lista en cadena separados por un patron especificado")
print(lista)
cadena="|".join(lista)
print(cadena)
print("replace: sustituye una parte de la cadena por contenido nuevo")
print(cadena.replace("|",";"))
print("startswith y endswith: respectivamente, indican si la cadena comienza o termina con determinado patron")
if cadena.startswith("0|1") and cadena.endswith("|8|9"):
    print(cadena+" empieza con 0|1 y termina con |8|9")
print("lower y upper: convierten las letras de una cadena a minuscula o mayuscula respectivamente")
cadena = ".:123hola321:."
upper=cadena.upper
print(cadena + " -> "+upper())
print("split: inverso de join, divide los caracteres de una cadena separados por un patron indicado y los almacena en una lista")
cadena =  "abracadabra"
lista = cadena.split("a")
print(cadena+".split(\"a\") produce lo siguiente: ")
print(lista)

print("Funciones numericas")
print("max,min,abs,sum: devuelve el maximo, minimo, valor absoluto y suma total en los elementos de una lista")
lista=[azar(-500,500) for r in range(10)]
print("lista = {0}".format(lista))
print("max(lista) = {0}".format(max(lista)))
print("min(lista) = {0}".format(min(lista)))
print("abs(lista[3]) = {0}".format(abs(lista[3])))
print("sum(lista) = {0}".format(sum(lista)))
print("round: establece un numero especifico de decimales para un entero")
print("round(pi,2) = round("+str(pi)+",2) = {0}".format(round(pi,2)))
       
print("Funciones en listas")
print("all y any: retornan True si todos o alguno, respectivamente, miembros de una lista cumplen con una determinada condicion")
print("Se usan comunmente en condicionales")
nums = [3*(x**3) for x in range(10)]
print("nums = {0}".format(nums))
if all(i >= 0 for i in nums):
    print("Todos los elementos de la lista nums son positivos o cero")
if any(i%2 != 0 for i in nums):
    print("Algunos de los elementos de la lista nums son impares")

print("enumerate: produce una iteracion con resultado indice,valor de una lista")
for x in enumerate(nums):
    print(x)

