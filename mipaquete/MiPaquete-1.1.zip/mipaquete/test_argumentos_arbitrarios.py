def function(argumento,*args):
    print(argumento)
    print(args)#Los argumentos arbitrarios se guardan como una tupla


def function2(x,y,z=1):
    print(x+y+z)#Argumentos predeterminados


def function3(x,y,z=1,*args,**kwargs):
    print(x+y+z)
    print(args)
    print(kwargs)
function(1,2,3,4,5,6)
function2(1,2)
function2(1,2,3)
function3(1,2,3,4,5,6,a=7,b=8,c=9,d=0)


