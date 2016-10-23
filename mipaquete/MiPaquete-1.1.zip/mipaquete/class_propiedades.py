#Propiedades
class Carro:
    def __init__(self,marca,anyo,modelo):
        self.marca=marca
        self.anyo=anyo
        self.modelo=modelo
        self._puertas=4

    @property
    def puertas(self):
        return self._puertas

    @puertas.setter
    def puertas(self,valor):
        if self.anyo == 2009 and valor == 2:
            self._puertas=valor
        else:
            raise ValueError("No se puede poner ese numero de puertas a un carro de ese año")

carro = Carro("Chevrolet",2008,"Aveo")

print("Ejemplo de propiedades")
print("Carro de marca {0}, año {1}, modelo {2}".format(carro.marca,carro.anyo,carro.modelo))
print("Ese carro tiene {0} puertas".format(carro._puertas))
try:
    carro.puertas=2
except AttributeError:
    print("No se puede decir que ese carro tiene 2 puertas")
except ValueError:
    print("No se puede decir que ese carro, para el año {0} tiene 2 puertas".format(carro.anyo))
    

carro.anyo=2009
print("El año fue  cambiado a {0}".format(carro.anyo))
try:
    carro.puertas = 2
except:
    print("Hubo un error estableciendo el numero de puertas")
print("Ese carro tiene {0} puertas".format(carro._puertas))

