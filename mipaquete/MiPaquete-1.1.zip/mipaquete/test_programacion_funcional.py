print((lambda x: x**2 +5*x +4)(-4))

nums = [11,22,33,44,55]

print("Ejemplo funcion map:")
print(list(map(lambda x: x**2 + 1,nums)))

print("Ejemplo funcion filter:")
print(list(filter(lambda x: x % 2 == 0,nums)))


print("Ejemplo generadores:")
def conteoregresivo():
    i = 5
    while i > 0:
        yield i
        i -= 1

for j in conteoregresivo():
    print(j)


print("Los generadores se pueden convertir en listas al pasarlos por la funcion list():")
def numeros(x):
    for i in range(x):
        if i % 2 == 0:
            yield i

print(list(numeros(11)))

print("Ejemplo 1 de decoradores:")
def decor(func):
    def wrap():
        print("==================")
        func()
        print("==================")
    return wrap

@decor
def hola_mundo():
    print("Hola mundo")

hola_mundo()

print("Ejemplo 2 de decoradores:")
def decorador(funcion):
    def interna(x):
        return funcion(x)**2
    return interna

def multipotencia(x):
    res = x**3
    return res

print("Funcion multipotencia(2) sin decorador:{0}".format(multipotencia(2)))
multipotencia = decorador(multipotencia)
print("Funcion multipotencia(2) con decorador:{0}".format(multipotencia(2)))

print("Ejemplo de recursion:")
def mi_funcion_recursiva(x):
    y = x[0]
    z = x
    if x == 32*y:
        return x
    else:
        z += x
        return x + mi_funcion_recursiva(z)

print(mi_funcion_recursiva("m"))

      
