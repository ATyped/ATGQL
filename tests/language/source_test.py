import pytest

from atgql.language.source import Location, Source


def test_asserts_that_a_body_was_provided():
    with pytest.raises(Exception, match='Body must be a string. Received: None.'):
        Source(None)  # type: ignore[arg-type]


def test_asserts_that_a_valid_body_was_provided():
    with pytest.raises(Exception, match='Body must be a string. Received: {}.'):
        Source({})  # type: ignore[arg-type]


def test_can_be_stringified():
    source = Source('')

    assert repr(source) == 'Source'


def test_rejects_invalid_location_offset():
    def create_source(location_offset: Location):
        return Source('', '', location_offset)

    with pytest.raises(
        Exception, match='line in location_offset is 1-indexed and must be positive.'
    ):
        create_source(Location(line=0, column=1))

    with pytest.raises(
        Exception, match='line in location_offset is 1-indexed and must be positive.'
    ):
        create_source(Location(line=-1, column=1))

    with pytest.raises(
        Exception, match='column in location_offset is 1-indexed and must be positive.'
    ):
        create_source(Location(line=1, column=0))

    with pytest.raises(
        Exception, match='column in location_offset is 1-indexed and must be positive.'
    ):
        create_source(Location(line=1, column=-1))
