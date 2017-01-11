import types
from inspect import getcallargs
from abc import abstractmethod
from collections import Iterable as IterableType

from decorator import decorator



class InputTypeError(TypeError):
    """
    TypeError raised when a runtime value is not the expected type
    """
    def __init__(self, name, value, expected_type):
        self.name = name
        self.expected_type = expected_type
        self.message = "Argument `{name}` is of type `{observed_type}`, not `{expected_type}`.".format(
            name=name,
            observed_type=type(value),
            expected_type=expected_type
        )
        super(TypeError, self).__init__(self.message)


class ReturnTypeError(TypeError):
    """
    TypeError raised when a runtime value is not the expected type
    """
    def __init__(self, expected_type, return_value):
        self.expected_type = expected_type
        self.message = "Return value is of type `{observed_type}`, not `{expected_type}`.".format(
            observed_type=type(return_value),
            expected_type=expected_type
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
                        raise InputTypeError(name, value, type_info[name])
                else:
                    raise InputTypeError(name, value, type_info[name])
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
                    raise ReturnTypeError(return_type, return_value)
            else:
                raise ReturnTypeError(return_type, return_value)
        return return_value
    return typed_fn


class BaseType(object):

    @abstractmethod
    def validate(self):
        raise NotImplementedError


class Any(BaseType):

    def __init__(self, *types):
        self.types = types

    def validate(self, value):
        return any((isinstance(value, _type) for _type in self.types))


class All(BaseType):

    def __init__(self, *types):
        self.types = types

    def validate(self, value):
        return all((isinstance(value, _type) for _type in self.types))


class Dict(BaseType):

    def __init__(self, key, value):
        self.key_type = key
        self.value_type = value

    def validate(self, value):
        return (
            isinstance(value, dict) and
            all([is_type(k, self.key_type) for k in value.iterkeys()]) and
            all([is_type(v, self.value_type) for v in value.itervalues()])
        )


class Iterable(BaseType):

    def __init__(self, item, iterable_type=IterableType):
        self.item_type = item
        self.iterable_type = iterable_type

    def validate(self, value):
        return (
            isinstance(value, self.iterable_type) and
            all([is_type(i, self.item_type) for i in value])
        )


class List(Iterable):

    def __init__(self, item):
        super(List, self).__init__(item, iterable_type=list)


class Tuple(Iterable):

    def __init__(self, item):
        super(Tuple, self).__init__(item, iterable_type=tuple)


class Set(Iterable):

    def __init__(self, item):
        super(Set, self).__init__(item, iterable_type=set)


def is_type(value, argtype):
    """
    Like isinstance, but also supports runtype's Or and And psuedotypes.
    """
    if isinstance(argtype, BaseType):
        return argtype.validate(value)
    else:
        return isinstance(value, argtype)
