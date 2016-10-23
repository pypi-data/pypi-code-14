class Animal:
    def __init__(self,patas,alas):
        self.patas=patas
        self.alas=alas
    def come(self):
        print("Yam")
    def  bebe(self):
        print("sup")

class Gallo(Animal):
    def kikiriki(self):
        print("kikiriki")

class Perro(Animal):
    def guau(self):
        print("guau")
    def come(self):#Ejemplo de sobrescritura de metodos heredados
        print ("Ñum!")

class Husky(Perro):#Ejemplo de herencia indirecta
    def rasca(self):
        print("Rasco")
        super().come()#Ejemplo de invocacion  del metodo padre con super

fido = Perro(4,0)
print("El perro tiene {0} patas".format(fido.patas))
fido.guau()
fido.come()
roos = Gallo(2,2)
print("El gallo tiene {0} patas y {1} alas".format(roos.patas,roos.alas))
roos.kikiriki()
husky = Husky(4,0)
print("El husky es una raza de perro que tiene {0} patas".format(husky.patas))
husky.guau()
husky.rasca()
husky.bebe()

