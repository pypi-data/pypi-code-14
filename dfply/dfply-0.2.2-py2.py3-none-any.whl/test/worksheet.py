from dfply import *

d = pd.DataFrame({
    'a':[1,2,3]
})

d >>= mutate(b=X.a*2) >> mutate(c=X.a+X.b) >> select(X.b, X.c)
print d



###
