from simplads.simplad_monad.simplad_monad import SimpladMonad
from simplads.simplad_monad.namedtuples.bind_args import BindArgs
from simplads.simplad_monad.namedtuples.simplad_result import SimpladResult
from simplads.simplads.reader_simplad import ReaderSimplad, ReaderDeltaMaker
from simplads.simplads.writer_simplad import WriterSimplad, WriterDeltaMaker

class SimpladBundle(object):
    def __init__(self):
        self.sm = SimpladMonad.make()
        self.init_deltas = {}

    def set_simplads(self, simplads):
        for key, simplad in simplads.iteritems():
            self.sm = SimpladMonad.push_simplad(
                simplad=simplad,
                key=key
            )(self.sm)
        return self

    def add_writer(self, obj):
        self.sm = SimpladMonad.push_simplad(
            key='writer', simplad=WriterSimplad())(self.sm)
        self.init_deltas['writer'] = WriterDeltaMaker.set_obj(obj)
        return self

    def add_reader(self, obj):
        self.sm = SimpladMonad.push_simplad(
            key='reader', simplad=ReaderSimplad())(self.sm)
        self.init_deltas['reader'] = ReaderDeltaMaker.set_obj(obj)
        return self

    def unit(self, unbound=None):
        self.bound = SimpladMonad.unit(self.sm)(unbound)
        self.run(SimpladBundle.delta_map(self.init_deltas))
        return self

    def pipe(self, funcs):
        bind_args = BindArgs(bound=self.bound, deltas=[])
        for func in funcs:
            self.sm, bind_args = SimpladMonad.bind(func)((self.sm, bind_args))
        self.bound = bind_args.bound
        return self.bound

    def run(self, func):
        bind_args = BindArgs(bound=self.bound, deltas=[])
        self.sm, bind_args = SimpladMonad.bind(func)((self.sm, bind_args))
        self.bound = bind_args.bound
        return self.bound

    @staticmethod
    def lift(func):
        return lambda i: SimpladResult(val=func(i), delta_map={})

    @staticmethod
    def res(val=None, delta_map={}):
        return SimpladResult(val=val, delta_map=delta_map)

    @staticmethod
    def echo(val, delta_map={}):
        return lambda i: SimpladBundle.res(val, delta_map)

    @staticmethod
    def delta_map(delta_map):
        return lambda i: SimpladBundle.res(i, delta_map)

    @staticmethod
    def delta(key, delta):
        return lambda i: SimpladBundle.res(i, {key: delta})
