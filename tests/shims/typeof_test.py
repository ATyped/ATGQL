from abc import ABC, abstractmethod
from types import MethodType

from atgql.shims import typeof


def test_typeof_builtin_constants():
    # https://docs.python.org/3/library/constants.html#built-in-consts
    assert typeof(False) == 'boolean'
    assert typeof(True) == 'boolean'
    assert typeof(None) == 'object'
    assert typeof(NotImplemented) == 'object'
    assert typeof(Ellipsis) == 'object'  # type: ignore[unreachable]
    assert typeof(...) == 'object'


def test_typeof_builtin_functions():
    # https://docs.python.org/3/library/functions.html#built-in-funcs
    assert typeof(abs) == 'function'
    assert typeof(all) == 'function'
    assert typeof(any) == 'function'
    assert typeof(ascii) == 'function'
    assert typeof(bin) == 'function'
    assert typeof(bool) == 'function'
    assert typeof(breakpoint) == 'function'
    assert typeof(callable) == 'function'
    assert typeof(bytearray) == 'function'
    assert typeof(bytes) == 'function'
    assert typeof(callable) == 'function'
    assert typeof(chr) == 'function'
    assert typeof(classmethod) == 'function'
    assert typeof(compile) == 'function'
    assert typeof(complex) == 'function'
    assert typeof(delattr) == 'function'
    assert typeof(dict) == 'function'
    assert typeof(dir) == 'function'
    assert typeof(divmod) == 'function'
    assert typeof(enumerate) == 'function'
    assert typeof(eval) == 'function'
    assert typeof(exec) == 'function'
    assert typeof(filter) == 'function'
    assert typeof(format) == 'function'
    assert typeof(frozenset) == 'function'
    assert typeof(getattr) == 'function'
    assert typeof(globals) == 'function'
    assert typeof(hasattr) == 'function'
    assert typeof(hash) == 'function'
    assert typeof(help) == 'function'
    assert typeof(hex) == 'function'
    assert typeof(id) == 'function'
    assert typeof(input) == 'function'
    assert typeof(isinstance) == 'function'
    assert typeof(issubclass) == 'function'
    assert typeof(iter) == 'function'
    assert typeof(len) == 'function'
    assert typeof(locals) == 'function'
    assert typeof(map) == 'function'
    assert typeof(max) == 'function'
    assert typeof(memoryview) == 'function'
    assert typeof(min) == 'function'
    assert typeof(next) == 'function'
    assert typeof(object) == 'function'
    assert typeof(oct) == 'function'
    assert typeof(open) == 'function'
    assert typeof(ord) == 'function'
    assert typeof(pow) == 'function'
    assert typeof(print) == 'function'
    assert typeof(property) == 'function'
    assert typeof(range) == 'function'
    assert typeof(repr) == 'function'
    assert typeof(reversed) == 'function'
    assert typeof(round) == 'function'
    assert typeof(set) == 'function'
    assert typeof(setattr) == 'function'
    assert typeof(slice) == 'function'
    assert typeof(sorted) == 'function'
    assert typeof(staticmethod) == 'function'
    assert typeof(str) == 'function'
    assert typeof(sum) == 'function'
    assert typeof(super) == 'function'
    assert typeof(tuple) == 'function'
    assert typeof(type) == 'function'
    assert typeof(vars) == 'function'
    assert typeof(zip) == 'function'
    assert typeof(__import__) == 'function'


def test_typeof_literals():
    assert typeof(1) == 'number'
    assert typeof(2.0) == 'number'
    assert typeof('3') == 'string'
    assert typeof([]) == 'object'
    assert typeof({}) == 'object'
    assert typeof((1,)) == 'object'
    assert typeof({1}) == 'object'


def test_typeof_str_subclass_instance_is_string():
    class Poetry(str):
        pass

    assert typeof(Poetry) == 'function'
    assert typeof(Poetry('poetry')) == 'string'


def test_typeof_number_subclass_instance_is_number():
    class Lumen(int):
        pass

    assert typeof(Lumen) == 'function'
    assert typeof(Lumen(2)) == 'number'

    class Meter(float):
        pass

    assert typeof(Meter) == 'function'
    assert typeof(Meter(2.333)) == 'number'


def test_typeof_function_is_function():
    def hello():
        ...

    assert typeof(hello) == 'function'


def test_typeof_class_is_function():
    class A:
        pass

    assert typeof(A) == 'function'


def test_typeof_bound_method_is_function():
    class A:
        def hello(self):
            pass

    assert typeof(A().hello) == 'function'
    assert typeof(MethodType(A.hello, A())) == 'function'
    assert typeof(A.hello.__get__(A())) == 'function'  # type: ignore[attr-defined]  # pylint: disable=no-value-for-parameter


def test_typeof_unbound_method_is_function():
    class A:
        def hello(self):
            pass

    assert typeof(A.hello) == 'function'


def test_typeof_staticmethod_is_function():
    class A:
        @staticmethod
        def hello():
            pass

    assert typeof(A.hello) == 'function'
    assert typeof(A().hello) == 'function'


def test_typeof_classmethod_is_function():
    class A:
        @classmethod
        def hello(cls):
            pass

    assert typeof(A.hello) == 'function'
    assert typeof(A().hello) == 'function'


def test_typeof_abstractmethod_is_function():
    class A(ABC):
        @staticmethod
        @abstractmethod
        def hello():
            pass

        @classmethod
        @abstractmethod
        def world(cls):
            pass

        @abstractmethod
        def python(self):
            pass

    assert typeof(A.hello) == 'function'
    assert typeof(A.world) == 'function'
    assert typeof(A.python) == 'function'
