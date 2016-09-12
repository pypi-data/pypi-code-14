from Object import Object


class Pete(Object):
    pass

class Flens(Object):
    pass

Pete._db_name  = 'Pete.db'
Flens._db_name = 'Pete.db'

x = Pete()
x.name = 'a'
x.save()


j = Flens()
j.anme = 'a'
j.save()