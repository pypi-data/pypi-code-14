import itertools as it
print("Las funciones count y cycle iteran infinitamente, con lo cual se debe gestionar la salida del bucle")
print("count(n)")
for i in it.count(3):
    print(i)
    if i>=11:
        break
print("cycle(iterable)")
for i in it.cycle(range(10)):
    print(i)
    if i >=7:
        break
print("repeat(o,n)")
for i in it.repeat("m",5):
    print(i)
print("accumulate: devuelve un total actualizado de valores ejecutados en un iterable")
nums = [10,20,30,40,50]
print(nums)
nums=list(it.accumulate(map(lambda x: x**2 + 1,nums)))
print(nums)

print("takewhile: toma un elemento de un iterable mientras que una funcion predicado permance verdadera")
print([i**2 for i in range(20) if i**2%2==0])
nums2 = list(it.takewhile(lambda t: t<=100,[i**2 for i in range(20) if i**2%2==0]))
print(nums2)

print("chain combina varios iterables en uno solo mas largo")
print(list(it.chain(nums,nums2)))

print("product y permutation: cumplir tareas con combinaciones posibles de elementos")
A=[2,4]
B=[3,6,9]
print("A:{0}".format(A))
print("B:{0}".format(B))
print("itertools.product(A,B):{0}".format(list(it.product(A,B))))
print("itertools.permutations(B):{0}".format(list(it.permutations(B))))

