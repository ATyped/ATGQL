from enum import Enum


class DirectiveLocation(str, Enum):
    """The set of allowed directive location values."""

    # Request Definitions

    QUERY = 'QUERY'
    MUTATION = 'MUTATION'
    SUBSCRIPTION = 'SUBSCRIPTION'
    FIELD = 'FIELD'
    FRAGMENT_DEFINITION = 'FRAGMENT_DEFINITION'
    FRAGMENT_SPREAD = 'FRAGMENT_SPREAD'
    INLINE_FRAGMENT = 'INLINE_FRAGMENT'
    VARIABLE_DEFINITION = 'VARIABLE_DEFINITION'

    # Type System Definitions

    SCHEMA = 'SCHEMA'
    SCALAR = 'SCALAR'
    OBJECT = 'OBJECT'
    FIELD_DEFINITION = 'FIELD_DEFINITION'
    ARGUMENT_DEFINITION = 'ARGUMENT_DEFINITION'
    INTERFACE = 'INTERFACE'
    UNION = 'UNION'
    ENUM = 'ENUM'
    ENUM_VALUE = 'ENUM_VALUE'
    INPUT_OBJECT = 'INPUT_OBJECT'
    INPUT_FIELD_DEFINITION = 'INPUT_FIELD_DEFINITION'


# The enum type representing the directive location values.
DirectiveLocationEnum = DirectiveLocation
