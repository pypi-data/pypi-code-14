import math
try:
    math.sqrt(-1)
    1/0
    "1"+2
except ZeroDivisionError:
    print("Ocurrió una division entre cero")
except TypeError:
    print("Operacion no compatible entre variables de distinto tipo")
except ValueError:
    print("Ocurrio una operacion matematica con resultados inesperados")
    #raise NameError("Error de Nombre!")
finally:
    print("Mensaje en el bloque finally")


