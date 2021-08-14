from atgql.pyutils.identity_func import identity_func


def test_returns_the_first_argument_it_receives():
    assert identity_func(None) is None

    obj: dict = {}
    assert identity_func(obj) is obj
