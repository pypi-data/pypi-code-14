import sys
import ctypes
import inspect
import operator
import traceback
import pprint

if sys.version_info < (3, 0):
    from cStringIO import StringIO
    import new
    import __builtin__ as builtins
    from types import NoneType

else:
    from io import StringIO
    import builtins
    NoneType = type(None)




__all__ = []


def get_dict(obj):
    _get_dict = ctypes.pythonapi._PyObject_GetDictPtr
    _get_dict.restype = ctypes.POINTER(ctypes.py_object)
    _get_dict.argtypes = [ctypes.py_object]
    return _get_dict(obj).contents.value

def set_method_to_builtin(clazz, method_func, method_name=None):
    if sys.version_info < (3, 0):
        method_name = method_name or method_func.func_code.co_name
    else:
        method_name = method_name or method_func.__code__.co_name

    get_dict(clazz)[method_name] = method_func

def set_method_to_object(method_func, method_name=None):
    set_method_to_builtin(object, method_func, method_name)



# def gen_title_from_stack_info(stack_info):
#     ''' it will generate the title from stack info.

#     '''
#     text  = stack_info[-2][-1]
#     index = text.rfind(".")
#     return text[:index]+" :"

def gen_title_from_stack_info(stack_info, func_name):
    ''' it will generate the title from stack info.

    '''
    text  = stack_info[-2][-1]
    index = text.rfind("."+func_name)
    return text[:index]+" :"

def gen_line_info(frame):
    '''
        the parameter 'frame' will like:
        (<frame object at 0x7fb521c7c8e0>,
         '/Users/Colin/work/minitest/minitest/with_test.py',
         233,
         '<module>',
         ['    tself.jc.ppl()\n'],
         0)
    '''
    return 'File "%s", line %d, in %s:' % (frame[1], frame[2], frame[3])

def p(self, title=None, auto_get_title=True):
    self_func_name = 'p'
    result = self
    # if type(result) == NoneType:
    #     result = None
    if title:
        print("{0} {1}".format(title, result))
    else:
        if auto_get_title:
            title = gen_title_from_stack_info(
                traceback.extract_stack(), self_func_name)
            print("{0} {1}".format(title, result))
        else:
            print(result)
    return result

def pp(self, title=None, auto_get_title=True):
    self_func_name = 'pp'
    result = self
    # if type(result) == NoneType:
    #     result = None
    if title:
        print(title)
    else:
        if auto_get_title:
            print(gen_title_from_stack_info(
                traceback.extract_stack(), self_func_name))
    pprint.pprint(result)
    return result

def p_format(self):
    self_func_name = 'p_format'
    title = gen_title_from_stack_info(
        traceback.extract_stack(), self_func_name)
    return "{0} {1}".format(title, self)

def pp_format(self):
    self_func_name = 'pp_format'
    title = gen_title_from_stack_info(
        traceback.extract_stack(), self_func_name)
    return "{0}\n{1}".format(title, pprint.pformat(self))

def pl_format(self):
    self_func_name = 'pl_format'
    title = gen_title_from_stack_info(
        traceback.extract_stack(), self_func_name)
    current_frame = inspect.getouterframes(inspect.currentframe())[1]
    return "line info: {0}\n{1}\n{2}".format(gen_line_info(current_frame), title, self)

def ppl_format(self):
    self_func_name = 'ppl_format'
    title = gen_title_from_stack_info(
        traceback.extract_stack(), self_func_name)
    current_frame = inspect.getouterframes(inspect.currentframe())[1]
    return "line info: {0}\n{1}\n{2}".format(gen_line_info(current_frame), title, pprint.pformat(self))

def pl(self, title=None, auto_get_title=True):
    ''' p with line information including file full path and line number.
        Notice, it will print new line firstly, since in some case, 
        there will be other string before file path
        and some editor cannot jump to the location.
    '''
    self_func_name = 'pl'
    result = self
    current_frame = inspect.getouterframes(inspect.currentframe())[1]
    print('\n    '+gen_line_info(current_frame))

    if title:
        print(title, result)
    else:
        if auto_get_title:
            title = gen_title_from_stack_info(
                traceback.extract_stack(), self_func_name)
            print("{0} {1}".format(title, result))
        else:
            print(result)
    return result

def ppl(self, title=None, auto_get_title=True):
    ''' pp with line information including file full path and line number.
        Notice, it will print new line firstly, since in some case, 
        there will be other string before file path
        and some editor cannot jump to the location.
    '''
    self_func_name = 'ppl'
    result = self
    current_frame = inspect.getouterframes(inspect.currentframe())[1]
    print('\n    '+gen_line_info(current_frame))

    if title:
        print(title)
    else:
        if auto_get_title:
            print(gen_title_from_stack_info(
                traceback.extract_stack(), self_func_name))
    pprint.pprint(result)
    return result

def length(self):
    return len(self)

def size(self):
    return len(self)


def inject_musts_methods():
    # must use list(globals().iteritems()),
    # if just use globals().iteritems(), 
    # set_method_to_builtin(NoneType, classmethod(func), name) will not work,
    # since in iteration, globals() will change.
    if sys.version_info < (3, 0):
        globals_items = list(globals().iteritems())
    else:
        globals_items = list(globals().items())

    set_method_to_object(p)
    set_method_to_object(pp)
    set_method_to_object(pl)
    set_method_to_object(ppl)
    set_method_to_object(length)
    set_method_to_object(size)
    # for None
    set_method_to_builtin(NoneType, classmethod(p), 'p')
    set_method_to_builtin(NoneType, classmethod(pp), 'pp')
    set_method_to_builtin(NoneType, classmethod(pl), 'pl')
    set_method_to_builtin(NoneType, classmethod(ppl), 'ppl')
    # set_method_to_builtin(NoneType, classmethod(must_equal), 'must_equal')
    # set_method_to_builtin(type, p, 'p')



    set_method_to_object(p_format)
    set_method_to_builtin(NoneType, classmethod(p_format), 'p_format')
    set_method_to_object(pp_format)
    set_method_to_builtin(NoneType, classmethod(pp_format), 'pp_format')
    set_method_to_object(pl_format)
    set_method_to_builtin(NoneType, classmethod(pl_format), 'pl_format')
    set_method_to_object(ppl_format)
    set_method_to_builtin(NoneType, classmethod(ppl_format), 'ppl_format')


inject_musts_methods()

