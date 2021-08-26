from __future__ import annotations

from atgql.language.ast import (
    ASTNode,
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
)
from typing import Any, Callable, Optional, Protocol, TypeVar, Union
from collections.abc import Sequence

# ASTVisitor should be defined here according to graphql-js,
# but confined by Python's syntax, ASTNode cannot refer the types defined below,
# so their definition go down to the bottom of this file.


# Python doesn't have the syntax corresponding to the TypeScript's `keyof`,
# so these types can only be manually coded.
# In order to test that there is no missing type, a test has been coded.


class _NameVisitor(Protocol):
    name: ASTVisitFn[NameNode] | EnterLeaveVisitor[NameNode]


class _DocumentVisitor(Protocol):
    document: ASTVisitFn[DocumentNode] | EnterLeaveVisitor[DocumentNode]


class _OperationDefinitionVisitor(Protocol):
    operation_definition: ASTVisitFn[OperationDefinitionNode] | EnterLeaveVisitor[
        OperationDefinitionNode
    ]


class _VariableDefinitionVisitor(Protocol):
    variable_definition: ASTVisitFn[VariableDefinitionNode] | EnterLeaveVisitor[
        VariableDefinitionNode
    ]


class _VariableVisitor(Protocol):
    variable: ASTVisitFn[VariableNode] | EnterLeaveVisitor[VariableNode]


class _SelectionSetVisitor(Protocol):
    selection_set: ASTVisitFn[SelectionSetNode] | EnterLeaveVisitor[SelectionSetNode]


class _FieldVisitor(Protocol):
    field: ASTVisitFn[FieldNode] | EnterLeaveVisitor[FieldNode]


class _ArgumentVisitor(Protocol):
    argument: ASTVisitFn[ArgumentNode] | EnterLeaveVisitor[ArgumentNode]


class _FragmentSpreadVisitor(Protocol):
    fragment_spread: ASTVisitFn[FragmentSpreadNode] | EnterLeaveVisitor[FragmentSpreadNode]


class _InlineFragmentVisitor(Protocol):
    inline_fragment: ASTVisitFn[InlineFragmentNode] | EnterLeaveVisitor[InlineFragmentNode]


class _FragmentDefinitionVisitor(Protocol):
    fragment_definition: ASTVisitFn[FragmentDefinitionNode] | EnterLeaveVisitor[
        FragmentDefinitionNode
    ]


class _IntValueVisitor(Protocol):
    int_value: ASTVisitFn[IntValueNode] | EnterLeaveVisitor[IntValueNode]


class _FloatValueVisitor(Protocol):
    float_value: ASTVisitFn[FloatValueNode] | EnterLeaveVisitor[FloatValueNode]


class _StringValueVisitor(Protocol):
    string_value: ASTVisitFn[StringValueNode] | EnterLeaveVisitor[StringValueNode]


class _BooleanValueVisitor(Protocol):
    boolean_value: ASTVisitFn[BooleanValueNode] | EnterLeaveVisitor[BooleanValueNode]


class _NullValueVisitor(Protocol):
    null_value: ASTVisitFn[NullValueNode] | EnterLeaveVisitor[NullValueNode]


class _EnumValueVisitor(Protocol):
    enum_value: ASTVisitFn[EnumValueNode] | EnterLeaveVisitor[EnumValueNode]


class _ListValueVisitor(Protocol):
    list_value: ASTVisitFn[ListValueNode] | EnterLeaveVisitor[ListValueNode]


class _ObjectValueVisitor(Protocol):
    object_value: ASTVisitFn[ObjectValueNode] | EnterLeaveVisitor[ObjectValueNode]


class _ObjectFieldVisitor(Protocol):
    object_field: ASTVisitFn[ObjectFieldNode] | EnterLeaveVisitor[ObjectFieldNode]


class _DirectiveVisitor(Protocol):
    directive: ASTVisitFn[DirectiveNode] | EnterLeaveVisitor[DirectiveNode]


class _NamedTypeVisitor(Protocol):
    named_type: ASTVisitFn[NamedTypeNode] | EnterLeaveVisitor[NamedTypeNode]


class _ListTypeVisitor(Protocol):
    list_type: ASTVisitFn[ListTypeNode] | EnterLeaveVisitor[ListTypeNode]


class _NonNullTypeVisitor(Protocol):
    non_null_type: ASTVisitFn[NonNullTypeNode] | EnterLeaveVisitor[NonNullTypeNode]


class _SchemaDefinitionVisitor(Protocol):
    schema_definition: ASTVisitFn[SchemaDefinitionNode] | EnterLeaveVisitor[SchemaDefinitionNode]


class _OperationTypeDefinitionVisitor(Protocol):
    operation_type_definition: ASTVisitFn[OperationTypeDefinitionNode] | EnterLeaveVisitor[
        OperationTypeDefinitionNode
    ]


class _ScalarTypeDefinitionVisitor(Protocol):
    scalar_type_definition: ASTVisitFn[ScalarTypeDefinitionNode] | EnterLeaveVisitor[
        ScalarTypeDefinitionNode
    ]


class _ObjectTypeDefinitionVisitor(Protocol):
    object_type_definition: ASTVisitFn[ObjectTypeDefinitionNode] | EnterLeaveVisitor[
        ObjectTypeDefinitionNode
    ]


class _FieldDefinitionVisitor(Protocol):
    field_definition: ASTVisitFn[FieldDefinitionNode] | EnterLeaveVisitor[FieldDefinitionNode]


class _InputValueDefinitionVisitor(Protocol):
    input_value_definition: ASTVisitFn[InputValueDefinitionNode] | EnterLeaveVisitor[
        InputValueDefinitionNode
    ]


class _InterfaceTypeDefinitionVisitor(Protocol):
    interface_type_definition: ASTVisitFn[InterfaceTypeDefinitionNode] | EnterLeaveVisitor[
        InterfaceTypeDefinitionNode
    ]


class _UnionTypeDefinitionVisitor(Protocol):
    union_type_definition: ASTVisitFn[UnionTypeDefinitionNode] | EnterLeaveVisitor[
        UnionTypeDefinitionNode
    ]


class _EnumTypeDefinitionVisitor(Protocol):
    enum_type_definition: ASTVisitFn[EnumTypeDefinitionNode] | EnterLeaveVisitor[
        EnumTypeDefinitionNode
    ]


class _EnumValueDefinitionVisitor(Protocol):
    enum_value_definition: ASTVisitFn[EnumValueDefinitionNode] | EnterLeaveVisitor[
        EnumValueDefinitionNode
    ]


class _InputObjectTypeDefinitionVisitor(Protocol):
    input_object_type_definition: ASTVisitFn[InputObjectTypeDefinitionNode] | EnterLeaveVisitor[
        InputObjectTypeDefinitionNode
    ]


class _DirectiveDefinitionVisitor(Protocol):
    directive_definition: ASTVisitFn[DirectiveDefinitionNode] | EnterLeaveVisitor[
        DirectiveDefinitionNode
    ]


class _SchemaExtensionVisitor(Protocol):
    schema_extension: ASTVisitFn[SchemaExtensionNode] | EnterLeaveVisitor[SchemaExtensionNode]


class _ScalarTypeExtensionVisitor(Protocol):
    scalar_type_extension: ASTVisitFn[ScalarTypeExtensionNode] | EnterLeaveVisitor[
        ScalarTypeExtensionNode
    ]


class _ObjectTypeExtensionVisitor(Protocol):
    object_type_extension: ASTVisitFn[ObjectTypeExtensionNode] | EnterLeaveVisitor[
        ObjectTypeExtensionNode
    ]


class _InterfaceTypeExtensionVisitor(Protocol):
    interface_type_extension: ASTVisitFn[InterfaceTypeExtensionNode] | EnterLeaveVisitor[
        InterfaceTypeExtensionNode
    ]


class _UnionTypeExtensionVisitor(Protocol):
    union_type_extension: ASTVisitFn[UnionTypeExtensionNode] | EnterLeaveVisitor[
        UnionTypeExtensionNode
    ]


class _EnumTypeExtensionVisitor(Protocol):
    enum_type_extension: ASTVisitFn[EnumTypeExtensionNode] | EnterLeaveVisitor[
        EnumTypeExtensionNode
    ]


class _InputObjectTypeExtensionVisitor(Protocol):
    input_object_type_extension: ASTVisitFn[InputObjectTypeExtensionNode] | EnterLeaveVisitor[
        InputObjectTypeExtensionNode
    ]


KindVisitor = Union[
    _NameVisitor,
    _DocumentVisitor,
    _OperationDefinitionVisitor,
    _VariableDefinitionVisitor,
    _VariableVisitor,
    _SelectionSetVisitor,
    _FieldVisitor,
    _ArgumentVisitor,
    _FragmentSpreadVisitor,
    _InlineFragmentVisitor,
    _FragmentDefinitionVisitor,
    _IntValueVisitor,
    _FloatValueVisitor,
    _StringValueVisitor,
    _BooleanValueVisitor,
    _NullValueVisitor,
    _EnumValueVisitor,
    _ListValueVisitor,
    _ObjectValueVisitor,
    _ObjectFieldVisitor,
    _DirectiveVisitor,
    _NamedTypeVisitor,
    _ListTypeVisitor,
    _NonNullTypeVisitor,
    _SchemaDefinitionVisitor,
    _OperationTypeDefinitionVisitor,
    _ScalarTypeDefinitionVisitor,
    _ObjectTypeDefinitionVisitor,
    _FieldDefinitionVisitor,
    _InputValueDefinitionVisitor,
    _InterfaceTypeDefinitionVisitor,
    _UnionTypeDefinitionVisitor,
    _EnumTypeDefinitionVisitor,
    _EnumValueDefinitionVisitor,
    _InputObjectTypeDefinitionVisitor,
    _DirectiveDefinitionVisitor,
    _SchemaExtensionVisitor,
    _ScalarTypeExtensionVisitor,
    _ObjectTypeExtensionVisitor,
    _InterfaceTypeExtensionVisitor,
    _UnionTypeExtensionVisitor,
    _EnumTypeExtensionVisitor,
    _InputObjectTypeExtensionVisitor,
]


TVisitedNode = TypeVar('TVisitedNode', bound=ASTNode, covariant=True)


class _EnterVisitor(Protocol[TVisitedNode]):
    enter: ASTVisitFn[TVisitedNode]


class _LeaveVisitor(Protocol[TVisitedNode]):
    leave: ASTVisitFn[TVisitedNode]


EnterLeaveVisitor = Union[_EnterVisitor[TVisitedNode], _LeaveVisitor[TVisitedNode]]


# The reason why not define ASTVisitFn as Protocol, is that ASTVisitFn use TVisitedNode as argument,
# which means convariant TVisitedNode must be contravariant.

# A visitor is comprised of visit functions, which are called on each node
# during the visitor's traversal.
ASTVisitFn = Callable[
    [
        # node
        # The current node being visiting.
        TVisitedNode,
        # key
        # The index or key to this node from the parent node or Array.
        Optional[str | int],
        # parent
        # The parent immediately above this node, which may be an Array.
        Optional[ASTNode],
        # path
        # The key path to get to this node from the root node.
        Sequence[str | int],
        # ancestors
        # All nodes and Arrays visited before reaching parent of this node.
        # These correspond to array indices in `path`.
        # Note: ancestors includes arrays which contain the parent of visited node.
        Sequence[ASTNode | Sequence[ASTNode]],
    ],
    Any,
]

ASTNodeType = TypeVar('ASTNodeType', bound=ASTNode)
R = TypeVar('R')


class _NodeReducerWithEnter(Protocol[ASTNodeType, R]):
    enter: ASTVisitFn[ASTNodeType]
    leave: ASTReducerFn[ASTNodeType, R]


class _NodeReducerWithoutEnter(Protocol[ASTNodeType, R]):
    leave: ASTReducerFn[ASTNodeType, R]


_NodeReducer = Union[_NodeReducerWithEnter, _NodeReducerWithoutEnter]


class _NameReducer(Protocol):
    name: _NodeReducer[NameNode]


class _DocumentReducer(Protocol):
    document: _NodeReducer[DocumentNode]


class _OperationDefinitionReducer(Protocol):
    operation_definition: _NodeReducer[OperationDefinitionNode]


class _VariableDefinitionReducer(Protocol):
    variable_definition: _NodeReducer[VariableDefinitionNode]


class _VariableReducer(Protocol):
    variable: _NodeReducer[VariableNode]


class _SelectionSetReducer(Protocol):
    selection_set: _NodeReducer[SelectionSetNode]


class _FieldReducer(Protocol):
    field: _NodeReducer[FieldNode]


class _ArgumentReducer(Protocol):
    argument: _NodeReducer[ArgumentNode]


class _FragmentSpreadReducer(Protocol):
    fragment_spread: _NodeReducer[FragmentSpreadNode]


class _InlineFragmentReducer(Protocol):
    inline_fragment: _NodeReducer[InlineFragmentNode]


class _FragmentDefinitionReducer(Protocol):
    fragment_definition: _NodeReducer[FragmentDefinitionNode]


class _IntValueReducer(Protocol):
    int_value: _NodeReducer[IntValueNode]


class _FloatValueReducer(Protocol):
    float_value: _NodeReducer[FloatValueNode]


class _StringValueReducer(Protocol):
    string_value: _NodeReducer[StringValueNode]


class _BooleanValueReducer(Protocol):
    boolean_value: _NodeReducer[BooleanValueNode]


class _NullValueReducer(Protocol):
    null_value: _NodeReducer[NullValueNode]


class _EnumValueReducer(Protocol):
    enum_value: _NodeReducer[EnumValueNode]


class _ListValueReducer(Protocol):
    list_value: _NodeReducer[ListValueNode]


class _ObjectValueReducer(Protocol):
    object_value: _NodeReducer[ObjectValueNode]


class _ObjectFieldReducer(Protocol):
    object_field: _NodeReducer[ObjectFieldNode]


class _DirectiveReducer(Protocol):
    directive: _NodeReducer[DirectiveNode]


class _NamedTypeReducer(Protocol):
    named_type: _NodeReducer[NamedTypeNode]


class _ListTypeReducer(Protocol):
    list_type: _NodeReducer[ListTypeNode]


class _NonNullTypeReducer(Protocol):
    non_null_type: _NodeReducer[NonNullTypeNode]


class _SchemaDefinitionReducer(Protocol):
    schema_definition: _NodeReducer[SchemaDefinitionNode]


class _OperationTypeDefinitionReducer(Protocol):
    operation_type_definition: _NodeReducer[OperationTypeDefinitionNode]


class _ScalarTypeDefinitionReducer(Protocol):
    scalar_type_definition: _NodeReducer[ScalarTypeDefinitionNode]


class _ObjectTypeDefinitionReducer(Protocol):
    object_type_definition: _NodeReducer[ObjectTypeDefinitionNode]


class _FieldDefinitionReducer(Protocol):
    field_definition: _NodeReducer[FieldDefinitionNode]


class _InputValueDefinitionReducer(Protocol):
    input_value_definition: _NodeReducer[InputValueDefinitionNode]


class _InterfaceTypeDefinitionReducer(Protocol):
    interface_type_definition: _NodeReducer[InterfaceTypeDefinitionNode]


class _UnionTypeDefinitionReducer(Protocol):
    union_type_definition: _NodeReducer[UnionTypeDefinitionNode]


class _EnumTypeDefinitionReducer(Protocol):
    enum_type_definition: _NodeReducer[EnumTypeDefinitionNode]


class _EnumValueDefinitionReducer(Protocol):
    enum_value_definition: _NodeReducer[EnumValueDefinitionNode]


class _InputObjectTypeDefinitionReducer(Protocol):
    input_object_type_definition: _NodeReducer[InputObjectTypeDefinitionNode]


class _DirectiveDefinitionReducer(Protocol):
    directive_definition: _NodeReducer[DirectiveDefinitionNode]


class _SchemaExtensionReducer(Protocol):
    schema_extension: _NodeReducer[SchemaExtensionNode]


class _ScalarTypeExtensionReducer(Protocol):
    scalar_type_extension: _NodeReducer[ScalarTypeExtensionNode]


class _ObjectTypeExtensionReducer(Protocol):
    object_type_extension: _NodeReducer[ObjectTypeExtensionNode]


class _InterfaceTypeExtensionReducer(Protocol):
    interface_type_extension: _NodeReducer[InterfaceTypeExtensionNode]


class _UnionTypeExtensionReducer(Protocol):
    union_type_extension: _NodeReducer[UnionTypeExtensionNode]


class _EnumTypeExtensionReducer(Protocol):
    enum_type_extension: _NodeReducer[EnumTypeExtensionNode]


class _InputObjectTypeExtensionReducer(Protocol):
    input_object_type_extension: _NodeReducer[InputObjectTypeExtensionNode]


ASTReducer = Union[
    _NameReducer,
    _DocumentReducer,
    _OperationDefinitionReducer,
    _VariableDefinitionReducer,
    _VariableReducer,
    _SelectionSetReducer,
    _FieldReducer,
    _ArgumentReducer,
    _FragmentSpreadReducer,
    _InlineFragmentReducer,
    _FragmentDefinitionReducer,
    _IntValueReducer,
    _FloatValueReducer,
    _StringValueReducer,
    _BooleanValueReducer,
    _NullValueReducer,
    _EnumValueReducer,
    _ListValueReducer,
    _ObjectValueReducer,
    _ObjectFieldReducer,
    _DirectiveReducer,
    _NamedTypeReducer,
    _ListTypeReducer,
    _NonNullTypeReducer,
    _SchemaDefinitionReducer,
    _OperationTypeDefinitionReducer,
    _ScalarTypeDefinitionReducer,
    _ObjectTypeDefinitionReducer,
    _FieldDefinitionReducer,
    _InputValueDefinitionReducer,
    _InterfaceTypeDefinitionReducer,
    _UnionTypeDefinitionReducer,
    _EnumTypeDefinitionReducer,
    _EnumValueDefinitionReducer,
    _InputObjectTypeDefinitionReducer,
    _DirectiveDefinitionReducer,
    _SchemaExtensionReducer,
    _ScalarTypeExtensionReducer,
    _ObjectTypeExtensionReducer,
    _InterfaceTypeExtensionReducer,
    _UnionTypeExtensionReducer,
    _EnumTypeExtensionReducer,
    _InputObjectTypeExtensionReducer,
]

TReducedNode = TypeVar('TReducedNode', bound=ASTNode, covariant=True)

ASTReducerFn = Callable[[],...]



# ASTVisitor should not be defined here according to graphql-js,
# but confined by Python's syntax, ASTNode can only refer the types defined above,
# so their definition settle down here.

# A visitor is provided to visit, it contains the collection of
# relevant functions to be called during the visitor's traversal.
ASTVisitor = Union[EnterLeaveVisitor[ASTNode], KindVisitor]
