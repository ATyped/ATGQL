from atgql.shims import typeof


def test_typeof_none_is_object():
    assert typeof(None) == 'object'


def test_typeof_str_subclass_instance_is_string():
    class Poetry(str):
        pass

    assert typeof(Poetry) == 'function'
    assert typeof(Poetry('poetry')) == 'string'


def test_typeof_builtin_type_instances():
    assert typeof(1) == 'number'
    assert typeo