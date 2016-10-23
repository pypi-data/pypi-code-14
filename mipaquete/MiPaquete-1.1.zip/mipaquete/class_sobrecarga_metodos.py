import random as ri
#metodos magicos y sobrecarga de operadores
class Vector2D:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __add__(self,other):#sobrecarga de operador  de suma
        return Vector2D(self.x+other.x,self.y+other.y)
class SpecialString:
    def __init__(self,cont):
        self.cont=cont

    def __truediv__(self,other):#sobrecarga de operador  de division
        line="="*len(other.cont)
        return "\n".join([self.cont,line,other.cont])

    def __gt__(self,other):
        for index in range(len(other.cont)+1):
            result = other.cont[:index] + ">" + self.cont
            result += ">" + other.cont[index:]
            print(result)

#metodos que imitan comportamiento de contenedores
class ListaVaga:
    def __init__(self,cont):
        self.cont=cont

    def __getitem__(self,index):
        return self.cont[index + ri.randint(-1,1)]

    def __len__(self):
        return ri.randint(0,len(self.cont)*2)


first  = Vector2D(5,7)
second = Vector2D(3,9)
result = first + second
print("first  = "+str(first.x)+","+str(first.y))
print("second = "+str(second.x)+","+str(second.y))
print("first + second = "+str(result.x)+","+str(result.y))

str1=SpecialString("Hola")
str2=SpecialString("Mundo")
print(str1/str2)
str1 > str2

lista_vaga=ListaVaga(["A","B","C","D","E"])
print(len(lista_vaga))
print(len(lista_vaga))
print(lista_vaga[2])
print(lista_vaga[2])
    
