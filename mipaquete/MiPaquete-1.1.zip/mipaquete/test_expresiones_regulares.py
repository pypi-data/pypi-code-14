import re
def coincide(objeto):
    if objeto == None:
        return  "(No coincide)"
    else:
        return "(Coincide)"
    
patron = r"cadena"
cadena="cadenaCadenaCADENAcADENA"
print("patron = \""+patron+"\"")
print("cadena = \""+cadena+"\"")
print("re.match busca el patron en el principio de la cadena")
if re.match(patron,cadena):
    print("cadena = \""+cadena+"\"")
    print("re.match(patron,cadena)")
    print("Coincide")
else:
    print("No Coincide")

print("re.search busca el patron en cualquier punto de la cadena")
cadena="esta es una cadena"
if re.search(patron,cadena):
    print("cadena = \""+cadena+"\"")
    print("re.search(patron,cadena)")
    print("La cadena tiene la palabra 'cadena' en ella")
    

print("re.findall devuelve una lista de todos los elementos en la cadena que coincidan con el patron")
cadena="La cadena que nos ata es una cadena debil"
print("cadena = \""+cadena+"\"")
print("re.findall(patron,cadena)=")
print(re.findall(patron,cadena))

print("re.finditer devuelve un iterable de todos los elementos en la cadena que coincidan con el patron")
print("re.finditer devuelve objetos MatchObject, no strings")
print("Funciones utiles de objetos MatchObject:")
print("start(): Numero donde comienza la coincidencia encontrada")
print("end(): Numero donde termina la coincidencia enontrada")
print("group(): Devuelve la cadena encontrada")
print("span(): Devuelve start() y end() en forma de tupla (a,b)")
it=list(re.finditer(patron,cadena))
print("cadena = \""+cadena+"\"")
print(" m.start(), m.end(), m.group(0), m.span()")
for m in it:
    print(" ",m.start(), m.end(), m.group(0), m.span())

print("re.sub reemplaza una parte de la cadena por otra cadena indicada")
cadena="0,1,2,3,4,5,6,7,8,9"
print("cadena = "+cadena)
print("re.sub(\",\",\"|\",cadena) = "+re.sub(",","|",cadena))

print("Metacaracteres")
print("Punto (.) : Coincidencia de cualquier caracter menos salto de linea")
cadena="mata,meta,mita,mota,muta"
patron=r"m.ta"
print("cadena = \""+cadena+"\"")
print("patron=r\"m.ta\"")
print("re.findall(patron,cadena)="+str(re.findall(patron,cadena)))

print("Se puede repetir varias veces")
cadena="mata,meca,misa,mofa,muda"
patron=r"m..a"
print("cadena = \""+cadena+"\"")
print("patron=r\"m..a\"")
print("re.findall(patron,cadena)="+str(re.findall(patron,cadena)))

print("Sombrero (^) y Dolar ($) : Indican que una cadena empiece y termine con un patron respectivamente (Menos salto de linea)")
cadena=["mata","mate","pata","masa"]
patron=r"^ma.a$"
print("cadena = "+str(cadena))
print("patron=r\"^ma.a$\"")
for cad in cadena:
    if re.match(patron,cad):
        con=" Coincide con el patron"
    else:
        con=" No coincide con el patron"        
    print("re.match(patron,\""+cad+"\")="+con)


print("Clases de Caracteres: Encerrados en corchetes, hacen coincidir")
print("la cadena con cualquier caracter dentro de la clase caracter")
cadena1="HOLAMUNDO"
cadena2="holamundo"
patron=r"[A-Z]"
print("patron = r\"[A-Z]\" : Busca en la cadena cualquier caracter con mayusculas")
if re.search(patron,cadena1):
    cad1=" Coincide con el patron"
else:
    cad1=" NO Coincide con el patron"
if re.search(patron,cadena2):
    cad2=" Coincide con el patron"
else:
    cad2=" No Coincide con el patron"
print("cadena1="+cadena1+"->re.search(patron,cadena1)="+cad1)
print("cadena2="+cadena2+"->re.search(patron,cadena2)="+cad2)

print("Ejemplo: Un patron que busque una cadena de tres caracteres, donde el primero este entre 'F' y 'J' mayusculas, el segundo entre 'n' y 'z' minusculas y el tercero sea un digito numerico")
patron=r"[F-J][n-z][0-9]"
print(patron)
cadena1="Go8"
cadena2="Am0"
cadena3="gO8"
print("cadena1="+cadena1)
print("cadena2="+cadena2)
print("cadena3="+cadena3)
if(re.match(patron,cadena1)):
   print("cadena1 coincide con el patron")
else:
   print("cadena1 no coincide con el patron")
if(re.match(patron,cadena2)):
   print("cadena2 coincide con el patron")
else:
   print("cadena2 no coincide con el patron")
if(re.match(patron,cadena3)):
   print("cadena3 coincide con el patron")
else:
   print("cadena3 no coincide con el patron")
print("Un caracter '^' justo despues del primer corchete de la clase de caracter invierte el significado de la misma")
print("Por ejemplo, el patron r\"[^A-Z]\" trae cualquier caracter menos letras mayusculas")

print("Mas metacaracteres")
print("* : Cero o mas repeticiones de lo anterior")
print("+ : Una o mas repeticiones de lo anterior")
print("? : Cero o una repeticion de lo anterior")
print("{numero1,numero2} : cantidad de repeticiones entre numero1 y numero2 de lo anterior")

patron1=r"(hola)*"
patron2=r"(chao)+"
patron3=r"test(-)?mio"
patron4=r"^j{2,3}$"

print("----------------------------------------------------")
cadena1="chola"
cadena2="alo"
print(patron1)
print(cadena1)
print(cadena2)
print(patron1,cadena1,coincide(re.search(patron1,cadena1)))
print(patron1,cadena2,coincide(re.search(patron1,cadena2)))
print("----------------------------------------------------")
cadena1="agachao"
cadena2="quedhao"
print(patron2)
print(cadena1)
print(cadena2)
print(patron2,cadena1,coincide(re.search(patron2,cadena1)))
print(patron2,cadena2,coincide(re.search(patron2,cadena2)))
print("----------------------------------------------------")
cadena1="testmio"
cadena2="test-mio"
print(patron3)
print(cadena1)
print(cadena2)
print(patron3,cadena1,coincide(re.search(patron3,cadena1)))
print(patron3,cadena2,coincide(re.search(patron3,cadena2)))
print("----------------------------------------------------")
cadena1="jj"
cadena2="jjjj"
print(patron4)
print(cadena1)
print(cadena2)
print(patron4,cadena1,coincide(re.search(patron4,cadena1)))
print(patron4,cadena2,coincide(re.search(patron4,cadena2)))
print("----------------------------------------------------")
patron1=r"a(bc)(de)(f(g)h)i"
patron2=r"(?P<primer_nombre>[A-Z][a-z]*) (?P<apellido>[A-Z][a-z]*)"
patron3=r"(?:hola) (?:mundo)"
patron4=r"(1|2|3|4|5)g"
print("Los grupos parentesis de una regex pueden ser accedidos con la funcion group(n)")
print("donde n es el grupo, si es 0, son todas las coincidencias,")
print("sin argumentos, son todas las coincidencias, mas de un argumento")
print("son tuplas de coincidencias")
cadena1="abcdefghi"
obj=re.search(patron1,cadena1)
print(cadena1,patron1)
print("group()="+obj.group())
print("group(0)="+obj.group(0))
print("group(1)="+obj.group(1))
print("group(2)="+obj.group(2))
print("group(3)="+obj.group(3))
print("group(3,1)="+str(obj.group(3,1)))
print("----------------------------------------------------")
print("En la regex se pueden crear grupos de la forma (?P<name>...))  con las cuales se crean grupos con nombres, e igualmente tienen un numero de grupo")
cadena2="Julio Munoz"
print(patron2,cadena2,coincide(re.search(patron2,cadena2)))
print("group(primer_nombre)="+re.search(patron2,cadena2).group("primer_nombre"))
print("group(apellido)="+re.search(patron2,cadena2).group("apellido"))
print("group(1)="+re.search(patron2,cadena2).group(1))
print("group(2)="+re.search(patron2,cadena2).group(2))
print("----------------------------------------------------")
print("En la regex se pueden crear grupos de la forma (?:...)  con las cuales se crean grupos que no generan ni nombre ni numero")
cadena3="hola mundo"
print(cadena3,patron3,coincide(re.search(patron3,cadena3)))
try:
    print("group(1)="+re.search(patron3,cadena3).group(1))
except:
    print("Los patrones de la forma (?:...)  generan grupos no numerados y/o anonimos")
print("groups()"+str(re.search(patron3,cadena3).groups()))
print("----------------------------------------------------")
print("El metacaracter '|' es usado como un or logico")
cadenas=["0g","1g","2g","3g","4g","5g","6g"]
print(str(cadenas))
for cadena in cadenas:
    print(cadena,patron4,coincide(re.search(patron4,cadena)))
print("----------------------------------------------------")
print("Secuencias Especiales")
print(r"\s coincide cualquier espacio en blanco. (En mayuscula es lo opuesto)")
print(r"\w coincide cualquier caracter alfanumerico. (En mayuscula es lo opuesto)")
print(r"\d coincide cualquier caracter numerico. (En mayuscula es lo opuesto)")
print(r"\(numero del  1 al 99) que el grupo de ese numero coincida con lo indicado en el patron ")
print(r"\b coincide cadena vacia entre caracteres \w o \W. (En mayuscula es lo opuesto)")
print(r"\A coincide principio de la cadena")
print(r"\Z coincide final de la cadena")
patron = r"(mi) (buen) (a...o) el (g..o)"
patron1 = r"(Hola\sJulio)"
cadena0="Hola_Julio"
cadena1="Hola Julio"
cadena2="mi buen amigo el gato"
print("group(1)="+re.search(patron1,cadena1).group(1))
try:
    print("group(1)="+re.search(patron1,cadena0).group(1))
except:
    print(cadena0+" no coincide con el patron "+patron1)
p=re.compile(patron)
print(p.search(cadena2).group(3))
