import types
from inspect import getcallargs

from decorator import decorator



class InputTypeError(TypeError):
    """
    TypeError raised when a runtime value is not the expected type
    """
    def __init__(self, name, argtype):
        self.name = name
        self.argtype = argtype
        self.message = "Argument `{name}` is not of type `{argtype}`.".format(
            name=name,
            argtype=argtype
        )
        super(TypeError, self).__init__(self.message)


class ReturnTypeError(TypeError):
    """
    TypeError raised when a runtime value is not the expected type
    """
    def __init__(self, argtype):
        self.argtype = argtype
        self.message = "Return value is not of type `{argtype}`.".format(
            argtype=argtype
        )
        super(TypeError, self).__init__(self.message)


def accepts(coerce_type=False, **type_info):
    """
    Input type checking decorator
    """
    @decorator
    def typed_fn(fn, *args, **kwargs):
        arguments = getcallargs(fn, *args, **kwargs)
        for name, value in arguments.iteritems():
            if name in type_info and not is_type(value, type_info[name]):
                if coerce_type:
                    try:
                        arguments[name] = type_info[name](value)
                    except Exception:
                        raise InputTypeError(name, type_info[name])
                else:
                    raise InputTypeError(name, type_info[name])
        return fn(**arguments)
    return typed_fn


def returns(return_type, coerce_type=False):
    """
    Return type type checking decorator
    """
    @decorator
    def typed_fn(fn, *args, **kwargs):
        return_value = fn(*args, **kwargs)
        if not is_type(return_value, return_type):
            if coerce_type:
                try:
                    return_value = return_type(return_value)
                except Exception:
                    raise ReturnTypeError(return_type)
            else:
                raise ReturnTypeError(return_type)
        return return_value
    return typed_fn


class Any(object):

    def __init__(self, *types):
        self.types = types


class All(object):
    
    def __init__(self, *types):
        self.types = types


def is_type(value, argtype):
    """
    Like isinstance, but also supports runtype's Or and And psuedotypes.
    """
    if isinstance(argtype, Any): 
        return any((isinstance(value, _type) for _type in argtype.types))
    elif isinstance(argtype, All):
        return all((isinstance(value, _type) for _type in argtype.types))
    else:
        return isinstance(value, argtype)
