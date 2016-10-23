class Persona:
    def __init__(self,nombre,apellido,edad):
        self.nombre=nombre
        self.apellido=apellido
        self.edad=edad

    def hola(self):
        print("Hola me llamo {0} {1}, tengo {2} años de edad".format(self.nombre,self.apellido,self.edad))


p = Persona("Julio","Muñoz",28)
p.hola()
