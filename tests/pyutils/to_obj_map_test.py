# Notice: These tests are not transformed from graphql-js

from collections.abc import Mapping
from dataclasses import dataclass

from atgql.pyutils.to_obj_map import to_obj_map


def test_convert_empty_object_to_obj_map():
    class Obj:
        ...

    result: Mapping = to_obj_map(Obj())
    assert result == {}


def test_convert_object_with_own_properties_to_obj_map():
    class Obj:
        def __init__(self: 'Obj'):
            self.foo = 'bar'

    assert to_obj_map(Obj()) == {'foo': 'bar'}


def test_convert_object_with_new_properties_to_obj_map():
    class Obj:
        pass

    obj = Obj()
    obj.foo = 'bar'  # type: ignore[attr-defined]

    assert to_obj_map(obj) == {'foo': 'bar'}


def test_convert_object_with_method_to_obj_map():
    class Obj:
        def hello(self):
            pass

    assert to_obj_map(Obj()) == {}


def test_convert_object_with_classmethod_to_obj_map():
    class Obj:
        @classmethod
        def hello(cls) -> None:
            pass

    assert to_obj_map(Obj()) == {}


def test_convert_object_with_staticmethod_to_obj_map():
    class Obj:
        @staticmethod
        def hello() -> None:
            pass

    assert to_obj_map(Obj()) == {}


def test_convert_object_with_class_var_to_obj_map():
    class Obj:
        foo = 'bar'

    assert to_obj_map(Obj()) == {}


def test_convert_object_with_base_classes_to_obj_map():
    class Base1:
        def __init__(self: 'Base1'):
            self.base_1 = 1

    class Base2:
        def __init__(self: 'Base2'):
            self.base_2 = 2

    class Obj(Base1, Base2):
        def __init__(self: 'Obj'):
            Base1.__init__(self)
            Base2.__init__(self)
            self.my = 3

    obj = Obj()

    assert to_obj_map(obj) == {'base_1': 1, 'base_2': 2, 'my': 3}


def test_convert_dataclass_to_obj_map():
    @dataclass
    class Obj:
        a: int = 1
        b: str = '2'

    assert to_obj_map(Obj()) == {'a': 1, 'b': '2'}
