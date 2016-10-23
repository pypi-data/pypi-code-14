print("Ejemplo de conjuntos (Similar a las listas  pero con elementos unicos):")
conj1 = {1,2,1,3,4,4,5,6,7,6,8,9,0}
conj2  = set(["hola","mundo","hola"])
print(conj1)
print(conj2)
print("Agregar con add:")
conj1.add(10)
conj2.add(10)

print(conj1)
print(conj2)
print("remover con pop y remove:")
conj1.pop()
conj2.remove(10)

print(conj1)
print(conj2)

print("Operadores en conjuntos:")
conj1 = {1,2,3,4,5,6}
conj2 = {4,5,6,7,8,9}

print("conj1 = ")
print(conj1)
print("conj2 = ")
print(conj2)
print("conj1|conj2 (Items de conj1 mas Items de conj2) = ")
print(conj1|conj2)      
print("conj1&conj2 (Items existentes tanto en conj1 como en conj2) = ")
print(conj1&conj2) 
print("conj1-conj2 (Items de conj1 menos existentes en conj2) = ")
print(conj1-conj2)
print("conj2-conj1 (Items de conj2 menos existentes en conj1) = ")
print(conj2-conj1)      
print("conj1^conj2 (Items en conj1 no existentes en conj2 mas Items en conj2 no existentes en conj1 ) = ")
print(conj1^conj2)      
