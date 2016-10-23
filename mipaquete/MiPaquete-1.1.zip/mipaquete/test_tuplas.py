tupla_1 = (1,2,3)

tupla_2 = "a","b","c"

try:
    tupla_2[0] = "d"
except:
    print("No se puede cambiar el valor de un elemento en una tupla")
