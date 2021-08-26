from __future__ import annotations


from dataclasses import dataclass, field, KW_ONLY
from enum import Enum
from typing import (
    Any,
    Final,
    Literal,
    Optional,
    TypeGuard,
    TypedDict,
    Union,
    cast,
    get_args,
)
from collections.abc import Sequence


from atgql.language.source import Source
from atgql.language.token_kind import TokenKindEnum


class Location:
    """
    Contains a range of UTF-8 character offsets and token references that
    identify the region of the source from which the AST derived.
    """

    # The character offset at which this Node begins.
    start: Final[int]  # pylint: disable=invalid-name

    # The character offset at which this Node ends.
    end: Final[int]  # pylint: disable=invalid-name

    # The Token at which this Node begins.
    start_token: Final[Token]  # pylint: disable=invalid-name

    # The Token at which this Node ends.
    end_token: Final[Token]  # pylint: disable=invalid-name

    # The Source document the AST represents.
    source: Final[Source]  # pylint: disable=invalid-name

    def __init__(self, start_token: Token, end_token: Token, source: Source) -> None:
        self.start = start_token.start
        self.end = end_token.end
        self.start_token = start_token
        self.end_token = end_token
        self.source = source

    class _LocationJson(TypedDict):
        start: int
        end: int

    def __json__(self) -> _LocationJson:
        return {'start': self.start, 'end': self.end}

    def __repr__(self) -> str:
        return 'Location'


class Token:
    """
    Represents a range of characters represented by a lexical token
    within a Source.
    """

    # The kind of Token.
    kind: Final[TokenKindEnum]  # pylint: disable=invalid-name

    # The character offset at which this Node begins.
    start: Final[int]  # pylint: disable=invalid-name

    # The character offset at which this Node ends.
    end: Final[int]  # pylint: disable=invalid-name

    # The 1-indexed line number on which this Token appears.
    line: Final[int]  # pylint: disable=invalid-name

    # The 1-indexed column number at which this Token begins.
    column: Final[int]  # pylint: disable=invalid-name

    # For non-punctuation tokens, represents the interpreted value of the token.
    #
    # Note: is undefined for punctuation tokens, but typed as string for
    # convenience in the parser.
    value: Final[str]  # pylint: disable=invalid-name

    # Tokens exist as nodes in a double-linked-list amongst all tokens
    # including ignored tokens. <SOF> is always the first node and <EOF>
    # the last.
    prev: Final[Optional[Token]]  # pylint: disable=invalid-name
    next: Final[Optional[Token]]  # pylint: disable=invalid-name

    def __init__(
        self,
        kind: TokenKindEnum,
        start: int,
        end: int,
        line: int,
        column: int,
        value: Optional[str],
    ) -> None:
        self.kind = kind
        self.start = start
        self.end = end
        self.line = line
        self.column = column
        self.value = cast(str, value)
        self.prev = None
        self.next = None

    class _TokenJson(TypedDict):
        kind: TokenKindEnum
        value: Optional[str]
        line: int
        column: int

    def __json__(self) -> _TokenJson:
        return {'kind': self.kind, 'value': self.value, 'line': self.line, 'column': self.column}

    def __repr__(self) -> str:
        return 'Token'


def is_node(maybe_node: Any) -> TypeGuard[ASTNode]:
    return isinstance(maybe_node, get_args(ASTNode))


# ASTNode and ASTKindToNode should be defined here according to graphql-js,
# but confined by Python's syntax, ASTNode cannot refer the types defined below,
# so their definition go down to the bottom of this file.


# Name


@dataclass(frozen=True)
class NameNode:
    _ = KW_ONLY
    kind: Literal['Name'] = field(default='Name', init=False)
    loc: Optional[Location]
    value: str


# Document


@dataclass(frozen=True)
class DocumentNode:
    _ = KW_ONLY
    kind: Literal['Document'] = field(default='Document', init=False)
    loc: Optional[Location]
    definitions: Sequence[DefinitionNode]


# DefinitionNode and ExecutableDefinitionNode should be defined here according to graphql-js,
# but confined by Python's syntax, ASTNode cannot refer the types defined below,
# so their definition go down to the bottom of this file.


@dataclass(frozen=True)
class OperationDefinitionNode:
    _ = KW_ONLY
    kind: Literal['OperationDefinition'] = field(default='OperationDefinition', init=False)
    loc: Optional[Location]
    operation: OperationTypeNode
    name: Optional[NameNode]
    variable_definitions: Optional[Sequence[VariableDefinitionNode]]
    directives: Optional[Sequence[DirectiveNode]]
    selection_set: SelectionSetNode


OperationTypeNode = Literal['query', 'mutation', 'subscription']


@dataclass(frozen=True)
class VariableDefinitionNode:
    _ = KW_ONLY
    kind: Literal['VariableDefinition'] = field(default='VariableDefinition', init=False)
    loc: Optional[Location]
    variable: VariableNode
    type: TypeNode
    default_value: Optional[ConstValueNode]
    directives: Optional[Sequence[ConstDirectiveNode]]


@dataclass(frozen=True)
class VariableNode:
    _ = KW_ONLY
    kind: Literal['Variable'] = field(default='Variable', init=False)
    loc: Optional[Location]
    name: NameNode


@dataclass(frozen=True)
class SelectionSetNode:
    _ = KW_ONLY
    kind: Literal['SelectionSet'] = field(default='SelectionSet', init=False)
    loc: Optional[Location]
    selections: Sequence[SelectionNode]


# SelectionNode should be defined here according to graphql-js,
# but confined by Python's syntax, ASTNode cannot refer the types defined below,
# so their definition go down to the bottom of this file.


@dataclass(frozen=True)
class FieldNode:
    _ = KW_ONLY
    kind: Literal['Field'] = field(default='Field', init=False)
    loc: Optional[Location]
    alias: Optional[NameNode]
    name: NameNode
    arguments: Optional[Sequence[ArgumentNode]]
    directives: Optional[Sequence[DirectiveNode]]
    selection_set: Optional[SelectionSetNode]


@dataclass(frozen=True)
class ArgumentNode:
    _ = KW_ONLY
    kind: Literal['Argument'] = field(default='Argument', init=False)
    loc: Optional[Location]
    name: NameNode
    value: ValueNode


@dataclass(frozen=True)
class ConstArgumentNode:
    _ = KW_ONLY
    kind: Literal['Argument'] = field(default='Argument', init=False)
    loc: Optional[Location]
    name: NameNode
    value: ConstValueNode


# Fragments


@dataclass(frozen=True)
class FragmentSpreadNode:
    _ = KW_ONLY
    kind: Literal['FragmentSpread'] = field(default='FragmentSpread', init=False)
    loc: Optional[Location]
    name: NameNode
    directives: Optional[Sequence[DirectiveNode]]


@dataclass(frozen=True)
class InlineFragmentNode:
    _ = KW_ONLY
    kind: Literal['InlineFragment'] = field(default='InlineFragment', init=False)
    loc: Optional[Location]
    type_condition: Optional[NamedTypeNode]
    directives: Optional[Sequence[DirectiveNode]]
    selection_set: SelectionSetNode


@dataclass(frozen=True)
class FragmentDefinitionNode:
    _ = KW_ONLY
    kind: Literal['FragmentDefinition'] = field(default='FragmentDefinition', init=False)
    loc: Optional[Location]
    name: NameNode
    # @deprecated variable_definitions will be removed in v17.0.0
    variable_definitions: Optional[Sequence[VariableDefinitionNode]]
    type_condition: NamedTypeNode
    directives: Optional[Sequence[DirectiveNode]]
    selection_set: SelectionSetNode


# Values


# ValueNode and ConstValueNode should be defined here according to graphql-js,
# but confined by Python's syntax, ASTNode cannot refer the types defined below,
# so their definition go down to the bottom of this file.


@dataclass(frozen=True)
class IntValueNode:
    _ = KW_ONLY
    kind: Literal['IntValue'] = field(default='IntValue', init=False)
    loc: Optional[Location]
    value: str


@dataclass(frozen=True)
class FloatValueNode:
    _ = KW_ONLY
    kind: Literal['FloatValue'] = field(default='FloatValue', init=False)
    loc: Optional[Location]
    value: str


@dataclass(frozen=True)
class StringValueNode:
    _ = KW_ONLY
    kind: Literal['StringValue'] = field(default='StringValue', init=False)
    loc: Optional[Location]
    value: str
    block: Optional[bool]


@dataclass(frozen=True)
class BooleanValueNode:
    _ = KW_ONLY
    kind: Literal['BoolValue'] = field(default='BoolValue', init=False)
    loc: Optional[Location]
    value: bool


@dataclass(frozen=True)
class NullValueNode:
    _ = KW_ONLY
    kind: Literal['NullValue'] = field(default='NullValue', init=False)
    loc: Optional[Location]


@dataclass(frozen=True)
class EnumValueNode:
    _ = KW_ONLY
    kind: Literal['EnumValue'] = field(default='EnumValue', init=False)
    loc: Optional[Location]
    value: str


@dataclass(frozen=True)
class ListValueNode:
    _ = KW_ONLY
    kind: Literal['ListValue'] = field(default='ListValue', init=False)
    loc: Optional[Location]
    values: Sequence[ValueNode]


@dataclass(frozen=True)
class ConstListValueNode:
    _ = KW_ONLY
    kind: Literal['ListValue'] = field(default='ListValue', init=False)
    loc: Optional[Location]
    values: Sequence[ConstValueNode]


@dataclass(frozen=True)
class ObjectValueNode:
    _ = KW_ONLY
    kind: Literal['ObjectValue'] = field(default='ObjectValue', init=False)
    loc: Optional[Location]
    fields: Sequence[ObjectFieldNode]


@dataclass(frozen=True)
class ConstObjectValueNode:
    _ = KW_ONLY
    kind: Literal['ObjectValue'] = field(default='ObjectValue', init=False)
    loc: Optional[Location]
    fields: Sequence[ConstObjectFieldNode]


@dataclass(frozen=True)
class ObjectFieldNode:
    _ = KW_ONLY
    kind: Literal['ObjectField'] = field(default='ObjectField', init=False)
    loc: Optional[Location]
    name: NameNode
    value: ValueNode


@dataclass(frozen=True)
class ConstObjectFieldNode:
    _ = KW_ONLY
    kind: Literal['ObjectField'] = field(default='ObjectField', init=False)
    loc: Optional[Location]
    name: NameNode
    value: ConstValueNode


# Directives


@dataclass(frozen=True)
class DirectiveNode:
    _ = KW_ONLY
    kind: Literal['Directive'] = field(default='Directive', init=False)
    loc: Optional[Location]
    name: NameNode
    arguments: Optional[Sequence[ArgumentNode]]


@dataclass(frozen=True)
class ConstDirectiveNode:
    _ = KW_ONLY
    kind: Literal['Directive'] = field(default='Directive', init=False)
    loc: Optional[Location]
    name: NameNode
    arguments: Optional[Sequence[ConstArgumentNode]]


# Type Reference

# TypeNode should be defined here according to graphql-js,
# but confined by Python's syntax, ASTNode cannot refer the types defined below,
# so their definition go down to the bottom of this file.


@dataclass(frozen=True)
class NamedTypeNode:
    _ = KW_ONLY
    kind: Literal['NamedType'] = field(default='NamedType', init=False)
    loc: Optional[Location]
    name: NameNode


@dataclass(frozen=True)
class ListTypeNode:
    _ = KW_ONLY
    kind: Literal['ListType'] = field(default='ListType', init=False)
    loc: Optional[Location]
    type: TypeNode


@dataclass(frozen=True)
class NonNullTypeNode:
    _ = KW_ONLY
    kind: Literal['NonNullType'] = field(default='NonNullType', init=False)
    loc: Optional[Location]
    type: Union[NamedTypeNode, ListTypeNode]


# Type System Definition


# TypeSystemDefinitionNode should be defined here according to graphql-js,
# but confined by Python's syntax, ASTNode cannot refer the types defined below,
# so their definition go down to the bottom of this file.


@dataclass(frozen=True)
class SchemaDefinitionNode:
    _ = KW_ONLY
    kind: Literal['SchemaDefinition'] = field(default='SchemaDefinition', init=False)
    loc: Optional[Location]
    description: Optional[StringValueNode]
    directives: Optional[Sequence[ConstDirectiveNode]]
    operation_types: Sequence[OperationTypeDefinitionNode]


@dataclass(frozen=True)
class OperationTypeDefinitionNode:
    _ = KW_ONLY
    kind: Literal['OperationTypeDefinition'] = field(default='OperationTypeDefinition', init=False)
    loc: Optional[Location]
    operation: OperationTypeNode
    type: NamedTypeNode


# Type Definition


# TypeDefinitionNode should be defined here according to graphql-js,
# but confined by Python's syntax, ASTNode cannot refer the types defined below,
# so their definition go down to the bottom of this file.


@dataclass(frozen=True)
class ScalarTypeDefinitionNode:
    _ = KW_ONLY
    kind: Literal['ScalarTypeDefinition'] = field(default='ScalarTypeDefinition', init=False)
    loc: Optional[Location]
    description: Optional[StringValueNode]
    name: NameNode
    directives: Optional[Sequence[ConstDirectiveNode]]


@dataclass(frozen=True)
class ObjectTypeDefinitionNode:
    _ = KW_ONLY
    kind: Literal['ObjectTypeDefinition'] = field(default='ObjectTypeDefinition', init=False)
    loc: Optional[Location]
    description: Optional[StringValueNode]
    name: NameNode
    interfaces: Optional[Sequence[NamedTypeNode]]
    directives: Optional[Sequence[ConstDirectiveNode]]
    fields: Optional[Sequence[FieldDefinitionNode]]


@dataclass(frozen=True)
class FieldDefinitionNode:
    _ = KW_ONLY
    kind: Literal['FieldDefinition'] = field(default='FieldDefinition', init=False)
    loc: Optional[Location]
    description: Optional[StringValueNode]
    name: NameNode
    arguments: Optional[Sequence[InputValueDefinitionNode]]
    type: TypeNode
    directives: Optional[Sequence[ConstDirectiveNode]]


@dataclass(frozen=True)
class InputValueDefinitionNode:
    _ = KW_ONLY
    kind: Literal['InputValueDefinition'] = field(default='InputValueDefinition', init=False)
    loc: Optional[Location]
    description: Optional[StringValueNode]
    name: NameNode
    type: TypeNode
    default_value: Optional[ConstValueNode]
    directives: Optional[Sequence[ConstDirectiveNode]]


@dataclass(frozen=True)
class InterfaceTypeDefinitionNode:
    _ = KW_ONLY
    kind: Literal['InterfaceTypeDefinition'] = field(default='InterfaceTypeDefinition', init=False)
    loc: Optional[Location]
    description: Optional[StringValueNode]
    name: NameNode
    interfaces: Optional[Sequence[NamedTypeNode]]
    directives: Optional[Sequence[ConstDirectiveNode]]
    fields: Optional[Sequence[FieldDefinitionNode]]


@dataclass(frozen=True)
class UnionTypeDefinitionNode:
    _ = KW_ONLY
    kind: Literal['UnionTypeDefinition'] = field(default='UnionTypeDefinition', init=False)
    loc: Optional[Location]
    description: Optional[StringValueNode]
    name: NameNode
    directives: Optional[Sequence[ConstDirectiveNode]]
    types: Optional[Sequence[NamedTypeNode]]


@dataclass(frozen=True)
class EnumTypeDefinitionNode:
    _ = KW_ONLY
    kind: Literal['EnumTypeDefinition'] = field(default='EnumTypeDefinition', init=False)
    loc: Optional[Location]
    description: Optional[StringValueNode]
    name: NameNode
    directives: Optional[Sequence[ConstDirectiveNode]]
    values: Optional[Sequence[EnumValueDefinitionNode]]


@dataclass(frozen=True)
class EnumValueDefinitionNode:
    _ = KW_ONLY
    kind: Literal['EnumValueDefinition'] = field(default='EnumValueDefinition', init=False)
    loc: Optional[Location]
    description: Optional[StringValueNode]
    name: NameNode
    directives: Optional[Sequence[ConstDirectiveNode]]


@dataclass(frozen=True)
class InputObjectTypeDefinitionNode:
    _ = KW_ONLY
    kind: Literal['InputObjectTypeDefinition'] = field(
        default='InputObjectTypeDefinition', init=False
    )
    loc: Optional[Location]
    description: Optional[StringValueNode]
    name: NameNode
    directives: Optional[Sequence[ConstDirectiveNode]]
    fields: Optional[Sequence[InputValueDefinitionNode]]


# Directive Definitions


@dataclass(frozen=True)
class DirectiveDefinitionNode:
    _ = KW_ONLY
    kind: Literal['DirectiveDefinition'] = field(default='DirectiveDefinition', init=False)
    loc: Optional[Location]
    description: Optional[StringValueNode]
    name: NameNode
    arguments: Optional[Sequence[InputValueDefinitionNode]]
    repeatable: bool
    locations: Sequence[NameNode]


# Type System Extensions

# TypeSystemExtensionNode should be defined here according to graphql-js,
# but confined by Python's syntax, ASTNode cannot refer the types defined below,
# so their definition go down to the bottom of this file.


@dataclass(frozen=True)
class SchemaExtensionNode:
    _ = KW_ONLY
    kind: Literal['SchemaExtension'] = field(default='SchemaExtension', init=False)
    loc: Optional[Location]
    directives: Optional[Sequence[ConstDirectiveNode]]
    operation_types: Optional[Sequence[OperationTypeDefinitionNode]]


# Type Extensions


# TypeExtensionNode should be defined here according to graphql-js,
# but confined by Python's syntax, ASTNode cannot refer the types defined below,
# so their definition go down to the bottom of this file.


@dataclass(frozen=True)
class ScalarTypeExtensionNode:
    _ = KW_ONLY
    kind: Literal['ScalarTypeExtension'] = field(default='ScalarTypeExtension', init=False)
    loc: Optional[Location]
    name: NameNode
    directives: Optional[Sequence[ConstDirectiveNode]]


@dataclass(frozen=True)
class ObjectTypeExtensionNode:
    _ = KW_ONLY
    kind: Literal['ObjectTypeExtension'] = field(default='ObjectTypeExtension', init=False)
    loc: Optional[Location]
    name: NameNode
    interfaces: Optional[Sequence[NamedTypeNode]]
    directives: Optional[Sequence[ConstDirectiveNode]]
    fields: Optional[Sequence[FieldDefinitionNode]]


@dataclass(frozen=True)
class InterfaceTypeExtensionNode:
    _ = KW_ONLY
    kind: Literal['InterfaceTypeExtension'] = field(default='InterfaceTypeExtension', init=False)
    loc: Optional[Location]
    name: NameNode
    interfaces: Optional[Sequence[NamedTypeNode]]
    directives: Optional[Sequence[ConstDirectiveNode]]
    fields: Optional[Sequence[FieldDefinitionNode]]


@dataclass(frozen=True)
class UnionTypeExtensionNode:
    _ = KW_ONLY
    kind: Literal['UnionTypeExtension'] = field(default='UnionTypeExtension', init=False)
    loc: Optional[Location]
    name: NameNode
    directives: Optional[Sequence[ConstDirectiveNode]]
    types: Optional[Sequence[NamedTypeNode]]


@dataclass(frozen=True)
class EnumTypeExtensionNode:
    _ = KW_ONLY
    kind: Literal['EnumTypeExtension'] = field(default='EnumTypeExtension', init=False)
    loc: Optional[Location]
    name: NameNode
    directives: Optional[Sequence[ConstDirectiveNode]]
    values: Optional[Sequence[EnumValueDefinitionNode]]


@dataclass(frozen=True)
class InputObjectTypeExtensionNode:
    _ = KW_ONLY
    kind: Literal['InputObjectTypeExtension'] = field(
        default='InputObjectTypeExtension', init=False
    )
    loc: Optional[Location]
    name: NameNode
    directives: Optional[Sequence[ConstDirectiveNode]]
    fields: Optional[Sequence[InputValueDefinitionNode]]


# TypeExtensionNode, TypeSystemExtensionNode, TypeDefinitionNode, TypeSystemDefinitionNode,
# TypeNode, ValueNode, ConstValueNode, SelectionNode, ExecutableDefinitionNode, DefinitionNode,
# ASTNode and ASTKindToNode should not be defined here according to graphql-js,
# but confined by Python's syntax, ASTNode can only refer the types defined above,
# so their definition settle down here.

TypeExtensionNode = Union[
    ScalarTypeExtensionNode,
    ObjectTypeExtensionNode,
    InterfaceTypeExtensionNode,
    UnionTypeExtensionNode,
    EnumTypeExtensionNode,
    InputObjectTypeExtensionNode,
]


TypeSystemExtensionNode = Union[SchemaExtensionNode, TypeExtensionNode]


TypeDefinitionNode = Union[
    ScalarTypeDefinitionNode,
    ObjectTypeDefinitionNode,
    InterfaceTypeDefinitionNode,
    UnionTypeDefinitionNode,
    EnumTypeDefinitionNode,
    InputObjectTypeDefinitionNode,
]


TypeSystemDefinitionNode = Union[SchemaDefinitionNode, TypeDefinitionNode, DirectiveDefinitionNode]


TypeNode = Union[NamedTypeNode, ListTypeNode, NonNullTypeNode]


ValueNode = Union[
    VariableNode,
    IntValueNode,
    FloatValueNode,
    StringValueNode,
    BooleanValueNode,
    NullValueNode,
    EnumValueNode,
    ListValueNode,
    ObjectValueNode,
]


ConstValueNode = Union[
    IntValueNode,
    FloatValueNode,
    StringValueNode,
    BooleanValueNode,
    NullValueNode,
    EnumValueNode,
    ConstListValueNode,
    ConstObjectValueNode,
]


SelectionNode = Union[FieldNode, FragmentSpreadNode, InlineFragmentNode]


ExecutableDefinitionNode = Union[OperationDefinitionNode, FragmentDefinitionNode]


DefinitionNode = Union[ExecutableDefinitionNode, TypeSystemDefinitionNode, TypeSystemExtensionNode]


# The list of all possible AST node types.
ASTNode = Union[
    NameNode,
    DocumentNode,
    OperationDefinitionNode,
    VariableDefinitionNode,
    VariableNode,
    SelectionSetNode,
    FieldNode,
    ArgumentNode,
    FragmentSpreadNode,
    InlineFragmentNode,
    FragmentDefinitionNode,
    IntValueNode,
    FloatValueNode,
    StringValueNode,
    BooleanValueNode,
    NullValueNode,
    EnumValueNode,
    ListValueNode,
    ObjectValueNode,
    ObjectFieldNode,
    DirectiveNode,
    NamedTypeNode,
    ListTypeNode,
    NonNullTypeNode,
    SchemaDefinitionNode,
    OperationTypeDefinitionNode,
    ScalarTypeDefinitionNode,
    ObjectTypeDefinitionNode,
    FieldDefinitionNode,
    InputValueDefinitionNode,
    InterfaceTypeDefinitionNode,
    UnionTypeDefinitionNode,
    EnumTypeDefinitionNode,
    EnumValueDefinitionNode,
    InputObjectTypeDefinitionNode,
    DirectiveDefinitionNode,
    SchemaExtensionNode,
    ScalarTypeExtensionNode,
    ObjectTypeExtensionNode,
    InterfaceTypeExtensionNode,
    UnionTypeExtensionNode,
    EnumTypeExtensionNode,
    InputObjectTypeExtensionNode,
]


class ASTKindToNode(Enum):
    """Utility type listing all nodes indexed by their kind."""

    Name = NameNode  # pylint: disable=invalid-name
    Document = DocumentNode  # pylint: disable=invalid-name
    OperationDefinition = OperationDefinitionNode  # pylint: disable=invalid-name
    VariableDefinition = VariableDefinitionNode  # pylint: disable=invalid-name
    Variable = VariableNode  # pylint: disable=invalid-name
    SelectionSet = SelectionSetNode  # pylint: disable=invalid-name
    Field = FieldNode  # pylint: disable=invalid-name
    Argument = ArgumentNode  # pylint: disable=invalid-name
    FragmentSpread = FragmentSpreadNode  # pylint: disable=invalid-name
    InlineFragment = InlineFragmentNode  # pylint: disable=invalid-name
    FragmentDefinition = FragmentDefinitionNode  # pylint: disable=invalid-name
    IntValue = IntValueNode  # pylint: disable=invalid-name
    FloatValue = FloatValueNode  # pylint: disable=invalid-name
    StringValue = StringValueNode  # pylint: disable=invalid-name
    BooleanValue = BooleanValueNode  # pylint: disable=invalid-name
    NullValue = NullValueNode  # pylint: disable=invalid-name
    EnumValue = EnumValueNode  # pylint: disable=invalid-name
    ListValue = ListValueNode  # pylint: disable=invalid-name
    ObjectValue = ObjectValueNode  # pylint: disable=invalid-name
    ObjectField = ObjectFieldNode  # pylint: disable=invalid-name
    Directive = DirectiveNode  # pylint: disable=invalid-name
    NamedType = NamedTypeNode  # pylint: disable=invalid-name
    ListType = ListTypeNode  # pylint: disable=invalid-name
    NonNullType = NonNullTypeNode  # pylint: disable=invalid-name
    SchemaDefinition = SchemaDefinitionNode  # pylint: disable=invalid-name
    OperationTypeDefinition = OperationTypeDefinitionNode  # pylint: disable=invalid-name
    ScalarTypeDefinition = ScalarTypeDefinitionNode  # pylint: disable=invalid-name
    ObjectTypeDefinition = ObjectTypeDefinitionNode  # pylint: disable=invalid-name
    FieldDefinition = FieldDefinitionNode  # pylint: disable=invalid-name
    InputValueDefinition = InputValueDefinitionNode  # pylint: disable=invalid-name
    InterfaceTypeDefinition = InterfaceTypeDefinitionNode  # pylint: disable=invalid-name
    UnionTypeDefinition = UnionTypeDefinitionNode  # pylint: disable=invalid-name
    EnumTypeDefinition = EnumTypeDefinitionNode  # pylint: disable=invalid-name
    EnumValueDefinition = EnumValueDefinitionNode  # pylint: disable=invalid-name
    InputObjectTypeDefinition = InputObjectTypeDefinitionNode  # pylint: disable=invalid-name
    DirectiveDefinition = DirectiveDefinitionNode  # pylint: disable=invalid-name
    SchemaExtension = SchemaExtensionNode  # pylint: disable=invalid-name
    ScalarTypeExtension = ScalarTypeExtensionNode  # pylint: disable=invalid-name
    ObjectTypeExtension = ObjectTypeExtensionNode  # pylint: disable=invalid-name
    InterfaceTypeExtension = InterfaceTypeExtensionNode  # pylint: disable=invalid-name
    UnionTypeExtension = UnionTypeExtensionNode  # pylint: disable=invalid-name
    EnumTypeExtension = EnumTypeExtensionNode  # pylint: disable=invalid-name
    InputObjectTypeExtension = InputObjectTypeExtensionNode  # pylint: disable=invalid-name
