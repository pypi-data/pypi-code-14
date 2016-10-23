#ocultamiento de informacion
#no existe el encapsulamiento como tal porque los atributos y metodos
#pueden ser accedidos desde fuera de la clase
#solo existenconvenciones de "debilmmente privado" y "fuertemente privado"

class Prueba:
    _a = 1
    __b =2
    def __init__(self,a):
        self.a=a


pr = Prueba(5)
print(pr.a)
print(pr._a)#acceso a variable "debilmente privada"
print(pr._Prueba__b)#acceso a variable "fuertemente privada"
