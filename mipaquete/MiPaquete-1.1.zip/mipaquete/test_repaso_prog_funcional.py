def suma(a,b):
    return a+b

def suma_multipl(func):
    def interna(a,b,c):
        return c*func(a,b)
    return interna

adicion=suma
adicion=suma_multipl(adicion)
print(adicion(3,4,7))
