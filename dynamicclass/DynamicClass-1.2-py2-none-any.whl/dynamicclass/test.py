from dynamicclass import DynamicClass

a = DynamicClass()
a.foo = 'foo'
a.sub.nome = 'test1'
a.subobject2.sub1.teste = 'test2'

assert a.foo == 'foo'
assert a.sub.nome == 'test1'
assert a.subobject2.sub1.teste == 'test2'

mydict = {
    'campo1': 'aaaa',
    'campo2': {
        'campo3': {
            'campo4': 'campo4'
        }
    },
    'lista': [
        {
            'item': '1',
            'desc': 'hello'
        },
        {
            'item': '2',
            'desc': 'olaa'
        }
    ]
}

b = DynamicClass(**mydict)

assert b.campo1 == 'aaaa'
assert b.campo2.campo3.campo4 == 'campo4'
assert b.lista[0].item == '1'
assert b.lista[1].item == '2'
