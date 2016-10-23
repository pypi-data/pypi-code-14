file = open("C:\\Users\\Public\\Desktop\\ejemplo.txt","w")
#Escribir
print("Escribir archivo")
print("Si el  2 argumento del constructor es \"w\" sobreescribe")
print("Si el  2 argumento del constructor es \"a\" añade al final")
print("Si el  2 argumento del constructor es \"b\" abre en binario")
for i in range(10):
    tmp = ""
    for j in range(10):
        if i == 0:
            tmp = tmp+"0"+str(j)+"|"
        else:
            tmp = tmp+str(10*i+j)+"|"
    file.write(tmp+chr(13)+chr(10))
file.close()

#Leer
print("Leer archivo forma 1:")
file = open("C:\\Users\\Public\\Desktop\\ejemplo.txt","r")
for line in file:
    print(line)
file.close()
print("Leer archivo forma 2, adicionalmente, gestion de cierre con bloque try/finally:")
try:
    file = open("C:\\Users\\Public\\Desktop\\ejemplo.txt","r")
    print(file.read())
finally:
    file.close()

print("Leer archivo forma 3, adicionalmente gestion de cierre en bloque with:")
with open("C:\\Users\\Public\\Desktop\\ejemplo.txt","r") as f:
    print(f.readlines())
