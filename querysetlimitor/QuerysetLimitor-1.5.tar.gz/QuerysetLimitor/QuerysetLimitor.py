from django.conf import settings

MAX_OBJ_NUM = getattr(settings, "MAX_OBJ_NUM",100000)

class QuerysetLimitor(object):

    def __init__(self,queryset,max_obj_num=MAX_OBJ_NUM):
        self._base_queryset = queryset
        self._generator = self._setup()
        self.max_obj_num = max_obj_num

    def _setup(self):
        for i in xrange(0,self._base_queryset.count(),self.max_obj_num):
            smaller_queryset = self._base_queryset[i:i+self.max_obj_num]
            for obj in smaller_queryset.iterator():
                yield obj

    def __iter__(self):
        return self

    def next(self):
        return self._generator.next()
