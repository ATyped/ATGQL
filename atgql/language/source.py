__all__ = ['Location', 'Source', 'is_source']

from dataclasses import dataclass
from typing import Any

from typing_extensions import TypeGuard

from atgql.pyutils.dev_assert import dev_assert
from atgql.pyutils.inspect_ import inspect
from atgql.pyutils.instance_of import instance_of
from atgql.shims import typeof


@dataclass(frozen=True)
class Location:
    line: int
    column: int


class Source:
    """
    A representation of source input to GraphQL. The `name` and `location_offset` parameters are
    optional, but they are useful for clients who store GraphQL documents in source files.
    For example, if the GraphQL input starts at line 40 in a file named `Foo.graphql`, it might
    be useful for `name` to be `"Foo.graphql"` and location to be `{ line: 40, column: 1 }`.
    The `line` and `column` properties in `location_offset` are 1-indexed.
    """

    body: str
    name: str
    location_offset: Location

    def __init__(
        self,
        body: str,
        name: str = 'GraphQL request',
        location_offset: Location = Location(line=1, column=1),
    ) -> None:
        dev_assert(typeof(body) == 'string', f'Body must be a string. Received: {inspect(body)}.')

        self.body = body
        self.name = name
        self.location_offset = location_offset
        dev_assert(
            self.location_offset.line > 0,
            'line in location_offset is 1-indexed and must be positive.',
        )
        dev_assert(
            self.location_offset.column > 0,
            'column in location_offset is 1-indexed and must be positive.',
        )

    def __repr__(self) -> str:
        return 'Source'


def is_source(source: Any) -> TypeGuard[Source]:
    return instance_of(source, Source)
