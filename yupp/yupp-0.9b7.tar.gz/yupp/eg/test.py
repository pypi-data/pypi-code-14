# coding: yupp

($set hola 'Hello yupp!')

#ops
print ($hola)


($set switch \cond.\case-eq..\case-cmp..\body.]
___cond = ($cond)
while True:
    ($body \case-eq \val.]
        if ___cond == ( ($val) ):
    [ \case-cmp \exp.]
        if ___cond ($exp):
    [ )
    break
[ )

pq = None
r = 0
q = 2

($switch (`pq) ]
    ($case-cmp,,is None)
        r = 100500
        break

    ($case-cmp,,== 3)
        r += 30;

    ($case-eq 2)
        r += 20;

    ($case-eq,,q)
        r += 1;
[ )

print r
