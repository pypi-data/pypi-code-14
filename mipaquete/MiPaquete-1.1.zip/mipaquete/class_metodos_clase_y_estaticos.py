class Rectangulo:
    def __init__(self,ancho,altura):
        self.ancho = ancho
        self.altura = altura

    def calc_area(self):
        return self.ancho*self.altura

    @classmethod
    def cuadrado(cls,lado):
        return cls(lado,lado)

cuadro =Rectangulo.cuadrado(5)
rectangulo = Rectangulo(3,4)
print("-------------Ejemplo de metodos de clase-------------------")
print("Area de cuadrado de lado 5 = {0}".format(cuadro.calc_area()))
print("Area de rectangulo 3x4 = {0}".format(rectangulo.calc_area()))


class Pizza:
    def __init__(self,topping):
        self.topping = topping

    @staticmethod
    def validar_topping(topping):
        if topping ==  "Pinya":
            raise ValueError("No se permiten pizzas de piña")
        else:
            return True

tops = ["Queso","Anchoas","Champinyones"]

print("----------------Ejemplo de metodos de estaticos-------------")
for top in tops:
    if Pizza.validar_topping(top):
        pizza = Pizza(top)
        print("Pizza de {0}".format(pizza.topping))
