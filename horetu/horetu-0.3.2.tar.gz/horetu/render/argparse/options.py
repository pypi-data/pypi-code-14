from ...signature import COUNT

def nargs(has_k2, step):
    if has_k2 and step == Step.keyword1:
        return '?'
    elif step == Step.var_positional:
        return '*'

def dest(param):
    if param.annotation in {list, COUNT} and param.default != param.empty:
        return singularize(param.name)

def action(step, param):
    if param.call == COUNT:
        return 'count'

    if step == Step.positional:
        return 'store'
    elif step in {Step.keyword1, Step.keyword2}:
#       print(param.call, 88)
        if param.call == None:
            if param.default == True:
                return 'store_false'
            elif param.default == False:
                return 'store_true'
            else:
                return 'store'
        elif param.call == bool:
            if param.default == True:
                return 'store_false'
            else:
                return 'store_true'
        elif param.call == list:
            return 'append'
        else:
            return 'store'
    elif step == Step.var_positional:
        return 'store'

from enum import Enum
class Step(Enum):
    positional = 1
    keyword1 = 2
    var_positional = 3
    keyword2 = 4

def choose_name_args(single_character_flags, has_k2, st, param):
    if st == Step.positional or (has_k2 and st == Step.keyword1):
        args = param.name,
    elif st in {Step.keyword1, Step.keyword2}:
        lf = longflag(param)
        sf = shortflag(param)
        if lf and sf in single_character_flags:
            args = lf,
        else:
            if lf:
                args = sf, lf
            else:
                args = sf,
    elif st == Step.var_positional:
        args = param.name,
    else:
        raise ValueError('Bad step: %s' % st)
    return args

