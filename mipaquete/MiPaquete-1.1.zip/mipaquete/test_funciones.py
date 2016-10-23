def reverse_string(cadena):
    """
    Ejemplo de  docstring
    Funcion que retorna el inverso  de un string
    """
    reverso = []
    for letra in cadena:
        reverso.append(letra)
    reverso.reverse()
    cadenaInv = ""
    for letraInv in reverso:
        cadenaInv = cadenaInv + letraInv
    return cadenaInv
def concatena_reversos(func,cadena1,cadena2):
    return func(cadena2)+func(cadena1)
    

cadenaEjemplo = "abcde"
cadenaEjemploReverso = reverse_string(cadenaEjemplo)
print(cadenaEjemploReverso)
print("Ejemplo de funciones como objetos:")
inversor = reverse_string
print(inversor("fghij"))
print("Ejemplo de funciones como argumento de otra funcion:")
print(concatena_reversos(inversor,"abcde","fghij"))
