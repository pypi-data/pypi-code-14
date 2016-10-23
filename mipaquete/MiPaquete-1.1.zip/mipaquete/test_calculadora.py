#Calculadora
while True:
    print("Ejemplo de calculadora basica")
    print("Introduzca la palabra suma,  para sumar 2 numeros")
    print("Introduzca la palabra resta,  para restar 2 numeros")
    print("Introduzca la palabra multi,  para multiplicar 2 numeros")
    print("Introduzca la palabra divi,  para dividir 2 numeros")
    print("Introduzca la palabra salir,  para salir del programa")
    user_input = input(": ")
    if user_input ==  "suma":
        num1=float(input("1er numero: "))
        num2=float(input("2do numero: "))
        print(num1+num2)
    elif user_input ==  "resta":
        num1=float(input("1er numero: "))
        num2=float(input("2do numero: "))
        print(num1-num2)
    elif user_input ==  "multi":
        num1=float(input("1er numero: "))
        num2=float(input("2do numero: "))
        print(num1*num2)
    elif user_input ==  "divi":
        num1=float(input("1er numero: "))
        num2=float(input("2do numero: "))
        print(num1/num2)
    elif user_input == "salir":
        break
    else:
        print(str(user_input)+" no valido!!! Lea las instrucciones")
    
