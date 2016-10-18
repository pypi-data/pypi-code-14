def myFunc():
    x=print('Hello from myFunc')
    y=print('Cool, eh?')
    return x, y, 2, 3, 'this'
#def print(*args, **kwargs): key word arguements
 #   return 'Ha ha!' 

#type hints or annotations ;; for documentation purposes! Useful! 
def myfunc2(name:str='Unknown', age:int=1, gender:str='Female') ->str:
    type(type(name))
    msg = 'Hello ' + str(name)
    msg += '. How are you today?'
    msg += '\nYou look good considering '
    msg += 'you are ' + str(age) + ' years old.'
    msg += '\nIt looks like you are ' + str(gender)
    msg += '.'
    return msg

def myfunc3(*args):         
    for arg in args:
        print(arg)

def myfunc4(**kwargs):
    for k, v in kwargs.items():
        print(k, '=>', v)


def myfunc5(*args, **kwargs):
    for arg in args:
        print(arg)
    for k, v in kwargs.items():
        print(k, '=>', v)
