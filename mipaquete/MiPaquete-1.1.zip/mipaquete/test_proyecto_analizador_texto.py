def contar_caracter(string,caracter):
    cantidad = 0
    for i in string:
        if i == caracter:
            cantidad += 1
    return cantidad

filename = input("Introduzca un nombre de archivo: ")
with open(filename) as f:
    text = f.read()

cadena = "abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ123456789,.-;:1234567890!\"·$%&/()=\r\n \t"
total = 0
for car in cadena:
    perc = 100*contar_caracter(text,car)/len(text)
    if car == " ":
        print("{0} - {1}%".format("\" \"",round(perc,3)))
    elif car == "\t":
        print("{0} - {1}%".format("\\t",round(perc,3)))
    elif car == "\r":
        print("{0} - {1}%".format("\\r",round(perc,3)))
    elif car == "\n":
        print("{0} - {1}%".format("\\n",round(perc,3)))
    else:        
        print("{0} - {1}%".format(car,round(perc,3)))
    total += perc
print("Total - "+str(total)+"%")
