from atgql.pyutils.instance_of import instance_of


def test_allows_instances_to_have_share_the_same_constructor_name():
    def get_minified_class(tag: str):
        class SomeNameAfterMinification:
            def __str__(self) -> str:
                return tag

        return SomeNameAfterMinification

    Foo = get_minified_class('Foo')
    Bar = get_minified_class('Bar')
    assert instance_of(Foo(), Bar) is False
    assert instance_of(Bar(), Foo) is False

    DuplicateOfFoo = get_minified_class('Foo')
    assert instance_of(DuplicateOfFoo(), Foo) is False
    assert instance_of(Foo(), DuplicateOfFoo) is False


# It shouldn't work in Python
def test_fails_with_descriptive_error_message() -> None:
    pass
