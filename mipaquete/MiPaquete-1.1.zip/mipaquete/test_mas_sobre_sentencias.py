#Else con ciclos (Se ejecuta si el ciclo termina de forma normal)
for i in range(10):
    if i == 999:
        break
else:
    print("Unbowed, Unbent, Unbroken")


try:
    print(1)
except:
    print(2)
else:
    print(3)
