import unittest
from numbers import Number

from runtype import (
    accepts, returns, InputTypeError, ReturnTypeError, Any, All,
    Dict, Iterable, List, Tuple, Set
)


@accepts(a=int, b=int)
def add_ints(a, b):
    return a + b


@accepts(a=int, b=int, coerce_type=True)
def coerce_type_and_add_ints(a, b):
    return a + b


@accepts(a=Any(int, float), b=Any(int, float))
def add_ints_or_floats(a, b):
    return a + b


@accepts(a=All(Number, int), b=All(Number, int))
def add_integers(a, b):
    return a + b


@returns(int)
def returns_int(a, b):
    return a + b


@returns(int, coerce_type=True)
def coerce_to_int_and_return(a, b):
    return a + b


@accepts(d=Dict(key=int, value=object))
def sum_keys(d):
    return sum(d.keys())


@accepts(l=List(int))
def sum_list(l):
    return sum(l)


@accepts(t=Tuple(int))
def sum_tuple(t):
    return sum(t)


@accepts(s=Set(int))
def sum_set_items(s):
    return sum(s)


@accepts(d=Dict(int, Dict(basestring, float)))
def nested_data_structure(d):
    return


class TypedTestCase(unittest.TestCase):

    def test_typed_fn(self):
        # ensure no error is raised and function behaves as intended
        assert add_ints(1, 2) == 3

        # ensure invalid types cause TypeErrors to be raised
        with self.assertRaises(InputTypeError):
            add_ints(1.0, 2.0)

    def test_type_coercion(self):
        # ensure type coercion works
        assert coerce_type_and_add_ints(1.0, 2.0) == 3

    def test_any(self):
        assert add_ints_or_floats(1, 2) == 3
        assert add_ints_or_floats(1, 2.0) == 3.0
        assert add_ints_or_floats(1.0, 2.0) == 3.0

        with self.assertRaises(InputTypeError):
            add_ints_or_floats(1, "two")

    def test_all(self):
        assert add_integers(1, 2) == 3

        with self.assertRaises(InputTypeError):
            add_integers(1.0, 2.0)

    def test_return_type(self):
        assert returns_int(1, 2) == 3

        with self.assertRaises(ReturnTypeError):
            returns_int(1.0, 2.0)

    def test_return_type_coercion(self):
        assert coerce_to_int_and_return(1.0, 2.0) == 3

        with self.assertRaises(ReturnTypeError):
            coerce_to_int_and_return("one", "two")

    def test_dict_type(self):
        assert sum_keys({1: "one", 2: "two"}) == 3

        with self.assertRaises(InputTypeError):
            sum_keys({1.0: "one", 2.0: "two"})

    def test_list_type(self):
        assert sum_list([1, 2]) == 3

        with self.assertRaises(InputTypeError):
            sum_list([1.0, 2.0])

    def test_tuple_type(self):
        assert sum_tuple((1, 2)) == 3

        with self.assertRaises(InputTypeError):
            sum_tuple((1.0, 2.0))

    def test_set_type(self):
        assert sum_set_items({1, 2}) == 3

        with self.assertRaises(InputTypeError):
            sum_set_items({1.0, 2.0})

    def test_nested_type(self):
        nested_data_structure({1: {"one": 1.0}})


        with self.assertRaises(InputTypeError):
            nested_data_structure({1: 1})

        with self.assertRaises(InputTypeError):
            nested_data_structure({1: {"one": "one"}})

        with self.assertRaises(InputTypeError):
            nested_data_structure({"one": {"one": 1}})
