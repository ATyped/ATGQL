from __future__ import annotations

from collections.abc import Sequence
from copy import copy
from dataclasses import dataclass
from typing import (
    Any,
    Callable,
    Final,
    Optional,
    Protocol,
    TypeVar,
    Union,
    cast,
    runtime_checkable,
)

from atgql.language.ast import (
    ArgumentNode,
    ASTNode,
    BooleanValueNode,
    DirectiveDefinitionNode,
    DirectiveNode,
    DocumentNode,
    EnumTypeDefinitionNode,
    EnumTypeExtensionNode,
    EnumValueDefinitionNode,
    EnumValueNode,
    FieldDefinitionNode,
    FieldNode,
    FloatValueNode,
    FragmentDefinitionNode,
    FragmentSpreadNode,
    InlineFragmentNode,
    InputObjectTypeDefinitionNode,
    InputObjectTypeExtensionNode,
    InputValueDefinitionNode,
    InterfaceTypeDefinitionNode,
    InterfaceTypeExtensionNode,
    IntValueNode,
    ListTypeNode,
    ListValueNode,
    NamedTypeNode,
    NameNode,
    NonNullTypeNode,
    NullValueNode,
    ObjectFieldNode,
    ObjectTypeDefinitionNode,
    ObjectTypeExtensionNode,
    ObjectValueNode,
    OperationDefinitionNode,
    OperationTypeDefinitionNode,
    ScalarTypeDefinitionNode,
    ScalarTypeExtensionNode,
    SchemaDefinitionNode,
    SchemaExtensionNode,
    SelectionSetNode,
    StringValueNode,
    UnionTypeDefinitionNode,
    UnionTypeExtensionNode,
    VariableDefinitionNode,
    VariableNode,
    is_node,
)
from atgql.pyutils.inspect_ import inspect
from atgql.shims import Array, UndefinedType, typeof, undefined

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


TVisitedNode = TypeVar('TVisitedNode', bound=ASTNode)


@runtime_checkable
class EnterVisitor(Protocol[TVisitedNode]):
    enter: ASTVisitFn[TVisitedNode]


@runtime_checkable
class LeaveVisitor(Protocol[TVisitedNode]):
    leave: ASTVisitFn[TVisitedNode]


EnterLeaveVisitor = Union[EnterVisitor[TVisitedNode], LeaveVisitor[TVisitedNode]]


# The reason why not define ASTVisitFn as Protocol, is that ASTVisitFn use TVisitedNode as argument,
# which means convariant TVisitedNode must be contravariant.

# A visitor is comprised of visit functions, which are called on each node
# during the visitor's traversal.
ASTVisitFn = Callable[
    [
        # self
        Any,
        # node
        # The current node being visiting.
        TVisitedNode,
        # key
        # The index or key to this node from the parent node or Array.
        Optional[Union[str, int]],
        # parent
        # The parent immediately above this node, which may be an Array.
        Optional[Union[ASTNode, list[ASTNode]]],
        # path
        # The key path to get to this node from the root node.
        Sequence[Union[str, int]],
        # ancestors
        # All nodes and Arrays visited before reaching parent of this node.
        # These correspond to array indices in `path`.
        # Note: ancestors includes arrays which contain the parent of visited node.
        Sequence[Union[ASTNode, Sequence[ASTNode]]],
    ],
    Any,
]

ASTNodeType = TypeVar('ASTNodeType', bound=ASTNode, covariant=True)
R = TypeVar('R')


# class _NodeReducerWithEnter(Protocol[ASTNodeType, R]):
#     enter: ASTVisitFn[ASTNodeType]
#     leave: ASTReducerFn[ASTNodeType, R]


# class _NodeReducerWithoutEnter(Protocol[ASTNodeType, R]):
#     leave: ASTReducerFn[ASTNodeType, R]


# _NodeReducer = Union[
#     _NodeReducerWithEnter[ASTNodeType, R], _NodeReducerWithoutEnter[ASTNodeType, R]
# ]


# class _NameReducer(Protocol[R]):
#     name: _NodeReducer[NameNode, R]


# class _DocumentReducer(Protocol[R]):
#     document: _NodeReducer[DocumentNode, R]


# class _OperationDefinitionReducer(Protocol[R]):
#     operation_definition: _NodeReducer[OperationDefinitionNode, R]


# class _VariableDefinitionReducer(Protocol[R]):
#     variable_definition: _NodeReducer[VariableDefinitionNode, R]


# class _VariableReducer(Protocol[R]):
#     variable: _NodeReducer[VariableNode, R]


# class _SelectionSetReducer(Protocol[R]):
#     selection_set: _NodeReducer[SelectionSetNode, R]


# class _FieldReducer(Protocol[R]):
#     field: _NodeReducer[FieldNode, R]


# class _ArgumentReducer(Protocol[R]):
#     argument: _NodeReducer[ArgumentNode, R]


# class _FragmentSpreadReducer(Protocol[R]):
#     fragment_spread: _NodeReducer[FragmentSpreadNode, R]


# class _InlineFragmentReducer(Protocol[R]):
#     inline_fragment: _NodeReducer[InlineFragmentNode, R]


# class _FragmentDefinitionReducer(Protocol[R]):
#     fragment_definition: _NodeReducer[FragmentDefinitionNode, R]


# class _IntValueReducer(Protocol[R]):
#     int_value: _NodeReducer[IntValueNode, R]


# class _FloatValueReducer(Protocol[R]):
#     float_value: _NodeReducer[FloatValueNode, R]


# class _StringValueReducer(Protocol[R]):
#     string_value: _NodeReducer[StringValueNode, R]


# class _BooleanValueReducer(Protocol[R]):
#     boolean_value: _NodeReducer[BooleanValueNode, R]


# class _NullValueReducer(Protocol[R]):
#     null_value: _NodeReducer[NullValueNode, R]


# class _EnumValueReducer(Protocol[R]):
#     enum_value: _NodeReducer[EnumValueNode, R]


# class _ListValueReducer(Protocol[R]):
#     list_value: _NodeReducer[ListValueNode, R]


# class _ObjectValueReducer(Protocol[R]):
#     object_value: _NodeReducer[ObjectValueNode, R]


# class _ObjectFieldReducer(Protocol[R]):
#     object_field: _NodeReducer[ObjectFieldNode, R]


# class _DirectiveReducer(Protocol[R]):
#     directive: _NodeReducer[DirectiveNode, R]


# class _NamedTypeReducer(Protocol[R]):
#     named_type: _NodeReducer[NamedTypeNode, R]


# class _ListTypeReducer(Protocol[R]):
#     list_type: _NodeReducer[ListTypeNode, R]


# class _NonNullTypeReducer(Protocol[R]):
#     non_null_type: _NodeReducer[NonNullTypeNode, R]


# class _SchemaDefinitionReducer(Protocol[R]):
#     schema_definition: _NodeReducer[SchemaDefinitionNode, R]


# class _OperationTypeDefinitionReducer(Protocol[R]):
#     operation_type_definition: _NodeReducer[OperationTypeDefinitionNode, R]


# class _ScalarTypeDefinitionReducer(Protocol[R]):
#     scalar_type_definition: _NodeReducer[ScalarTypeDefinitionNode, R]


# class _ObjectTypeDefinitionReducer(Protocol[R]):
#     object_type_definition: _NodeReducer[ObjectTypeDefinitionNode, R]


# class _FieldDefinitionReducer(Protocol[R]):
#     field_definition: _NodeReducer[FieldDefinitionNode, R]


# class _InputValueDefinitionReducer(Protocol[R]):
#     input_value_definition: _NodeReducer[InputValueDefinitionNode, R]


# class _InterfaceTypeDefinitionReducer(Protocol[R]):
#     interface_type_definition: _NodeReducer[InterfaceTypeDefinitionNode, R]


# class _UnionTypeDefinitionReducer(Protocol[R]):
#     union_type_definition: _NodeReducer[UnionTypeDefinitionNode, R]


# class _EnumTypeDefinitionReducer(Protocol[R]):
#     enum_type_definition: _NodeReducer[EnumTypeDefinitionNode, R]


# class _EnumValueDefinitionReducer(Protocol[R]):
#     enum_value_definition: _NodeReducer[EnumValueDefinitionNode, R]


# class _InputObjectTypeDefinitionReducer(Protocol[R]):
#     input_object_type_definition: _NodeReducer[InputObjectTypeDefinitionNode, R]


# class _DirectiveDefinitionReducer(Protocol[R]):
#     directive_definition: _NodeReducer[DirectiveDefinitionNode, R]


# class _SchemaExtensionReducer(Protocol[R]):
#     schema_extension: _NodeReducer[SchemaExtensionNode, R]


# class _ScalarTypeExtensionReducer(Protocol[R]):
#     scalar_type_extension: _NodeReducer[ScalarTypeExtensionNode, R]


# class _ObjectTypeExtensionReducer(Protocol[R]):
#     object_type_extension: _NodeReducer[ObjectTypeExtensionNode, R]


# class _InterfaceTypeExtensionReducer(Protocol[R]):
#     interface_type_extension: _NodeReducer[InterfaceTypeExtensionNode, R]


# class _UnionTypeExtensionReducer(Protocol[R]):
#     union_type_extension: _NodeReducer[UnionTypeExtensionNode, R]


# class _EnumTypeExtensionReducer(Protocol[R]):
#     enum_type_extension: _NodeReducer[EnumTypeExtensionNode, R]


# class _InputObjectTypeExtensionReducer(Protocol[R]):
#     input_object_type_extension: _NodeReducer[InputObjectTypeExtensionNode, R]


# ASTReducer = Union[
#     _NameReducer,
#     _DocumentReducer,
#     _OperationDefinitionReducer,
#     _VariableDefinitionReducer,
#     _VariableReducer,
#     _SelectionSetReducer,
#     _FieldReducer,
#     _ArgumentReducer,
#     _FragmentSpreadReducer,
#     _InlineFragmentReducer,
#     _FragmentDefinitionReducer,
#     _IntValueReducer,
#     _FloatValueReducer,
#     _StringValueReducer,
#     _BooleanValueReducer,
#     _NullValueReducer,
#     _EnumValueReducer,
#     _ListValueReducer,
#     _ObjectValueReducer,
#     _ObjectFieldReducer,
#     _DirectiveReducer,
#     _NamedTypeReducer,
#     _ListTypeReducer,
#     _NonNullTypeReducer,
#     _SchemaDefinitionReducer,
#     _OperationTypeDefinitionReducer,
#     _ScalarTypeDefinitionReducer,
#     _ObjectTypeDefinitionReducer,
#     _FieldDefinitionReducer,
#     _InputValueDefinitionReducer,
#     _InterfaceTypeDefinitionReducer,
#     _UnionTypeDefinitionReducer,
#     _EnumTypeDefinitionReducer,
#     _EnumValueDefinitionReducer,
#     _InputObjectTypeDefinitionReducer,
#     _DirectiveDefinitionReducer,
#     _SchemaExtensionReducer,
#     _ScalarTypeExtensionReducer,
#     _ObjectTypeExtensionReducer,
#     _InterfaceTypeExtensionReducer,
#     _UnionTypeExtensionReducer,
#     _EnumTypeExtensionReducer,
#     _InputObjectTypeExtensionReducer,
# ]

# TReducedNode = TypeVar('TReducedNode', bound=ASTNode, covariant=True)


# ASTReducerFn = Callable[
#     [
#         Any,
#         ASTNodeType,
#         Optional[str | int],
#         Optional[ASTNode | Sequence[ASTNode]],
#         Sequence[str | int],
#         Sequence[ASTNode | Sequence[ASTNode]],
#     ],
#     R,
# ]


# T = TypeVar('T')

# ReducedField = Union[Optional[T], Sequence[T], R]


query_document_keys: Final[dict[str, Sequence[str]]] = {
    'Name': [],
    'Document': ['definitions'],
    'OperationDefinition': ['name', 'variable_definitions', 'directives', 'selection_set'],
    'VariableDefinition': ['variable', 'type', 'default_value', 'directives'],
    'Variable': ['name'],
    'SelectionSet': ['selections'],
    'Field': ['alias', 'name', 'arguments', 'directives', 'selection_set'],
    'Argument': ['name', 'value'],
    'FragmentSpread': ['name', 'directives'],
    'InlineFragment': ['type_condition', 'directives', 'selection_set'],
    'FragmentDefinition': [
        'name',
        # Note: fragment variable definitions are deprecated and will removed in v17.0.0
        'variable_definitions',
        'type_condition',
        'directives',
        'selection_set',
    ],
    'IntValue': [],
    'FloatValue': [],
    'StringValue': [],
    'BooleanValue': [],
    'NullValue': [],
    'EnumValue': [],
    'ListValue': ['values'],
    'ObjectValue': ['fields'],
    'ObjectField': ['name', 'value'],
    'Directive': ['name', 'arguments'],
    'NamedType': ['name'],
    'ListType': ['type'],
    'NonNullType': ['type'],
    'SchemaDefinition': ['description', 'directives', 'operation_types'],
    'OperationTypeDefinition': ['type'],
    'ScalarTypeDefinition': ['description', 'name', 'directives'],
    'ObjectTypeDefinition': [
        'description',
        'name',
        'interfaces',
        'directives',
        'fields',
    ],
    'FieldDefinition': ['description', 'name', 'arguments', 'type', 'directives'],
    'InputValueDefinition': [
        'description',
        'name',
        'type',
        'default_value',
        'directives',
    ],
    'InterfaceTypeDefinition': [
        'description',
        'name',
        'interfaces',
        'directives',
        'fields',
    ],
    'UnionTypeDefinition': ['description', 'name', 'directives', 'types'],
    'EnumTypeDefinition': ['description', 'name', 'directives', 'values'],
    'EnumValueDefinition': ['description', 'name', 'directives'],
    'InputObjectTypeDefinition': ['description', 'name', 'directives', 'fields'],
    'DirectiveDefinition': ['description', 'name', 'arguments', 'locations'],
    'SchemaExtension': ['directives', 'operation_types'],
    'ScalarTypeExtension': ['name', 'directives'],
    'ObjectTypeExtension': ['name', 'interfaces', 'directives', 'fields'],
    'InterfaceTypeExtension': ['name', 'interfaces', 'directives', 'fields'],
    'UnionTypeExtension': ['name', 'directives', 'types'],
    'EnumTypeExtension': ['name', 'directives', 'values'],
    'InputObjectTypeExtension': ['name', 'directives', 'fields'],
}


class _BreakType:
    ...


BREAK: Final = _BreakType()


@dataclass
class _Stack:
    in_array: bool
    index: int
    keys: Union[Sequence[ASTNode], Sequence[str]]
    edits: list[tuple[Union[str, int], Any]]
    prev: Optional[_Stack]


def visit(root: ASTNode, visitor: ASTVisitor) -> ASTNode:
    """
    visit() will walk through an AST using a depth-first traversal, calling
    the visitor's enter function at each node in the traversal, and calling the
    leave function after visiting that node and all of its child nodes.

    By returning different values from the enter and leave functions, the
    behavior of the visitor can be altered, including skipping over a sub-tree of
    the AST (by returning false), editing the AST by returning a value or null
    to remove the value, or to stop the whole traversal by returning BREAK.

    When using visit() to edit an AST, the original AST will not be modified, and
    a new version of the AST with the changes applied will be returned from the
    visit function.

    ```ts
    const editedAST = visit(ast, {
      enter(node, key, parent, path, ancestors) {
        // @return
        //   undefined: no action
        //   false: skip visiting this node
        //   visitor.BREAK: stop visiting altogether
        //   null: delete this node
        //   any value: replace this node with the returned value
      },
      leave(node, key, parent, path, ancestors) {
        // @return
        //   undefined: no action
        //   false: no action
        //   visitor.BREAK: stop visiting altogether
        //   null: delete this node
        //   any value: replace this node with the returned value
      }
    });
    ```

    Alternatively to providing enter() and leave() functions, a visitor can
    instead provide functions named the same as the kinds of AST nodes, or
    enter/leave visitors at a named key, leading to three permutations of the
    visitor API:

    1) Named visitors triggered when entering a node of a specific kind.

    ```ts
    visit(ast, {
      Kind(node) {
        // enter the "Kind" node
      }
    })
    ```

    2) Named visitors that trigger upon entering and leaving a node of a specific kind.

    ```ts
    visit(ast, {
      Kind: {
        enter(node) {
          // enter the "Kind" node
        }
        leave(node) {
          // leave the "Kind" node
        }
      }
    })
    ```

    3) Generic visitors that trigger upon entering and leaving any node.

    ```ts
    visit(ast, {
      enter(node) {
        // enter any node
      },
      leave(node) {
        // leave any node
      }
    })
    ```
    """

    stack: Optional[_Stack] = None
    in_array = Array.is_array(root)
    keys: Union[Sequence[ASTNode], Sequence[str]] = [root]
    index = -1
    edits: list[tuple[Union[str, int], Any]] = []
    node: Optional[Union[list[ASTNode], ASTNode]] = None
    key: Optional[Union[str, int]] = None
    parent: Optional[Union[ASTNode, list[ASTNode]]] = None
    path: list[Union[str, int]] = []
    ancestors: list[Union[ASTNode, list[ASTNode]]] = []
    new_root = root

    while True:
        index += 1
        is_leaving = index == len(keys)
        is_edited = is_leaving and len(edits) != 0
        if is_leaving:
            # Type Guards
            assert isinstance(stack, _Stack)

            key = None if len(ancestors) == 0 else path[-1]
            node = parent
            parent = ancestors.pop()
            if is_edited:
                # node = node[:] if in_array else copy(node)
                if in_array:
                    # Type Guard
                    assert isinstance(node, list)

                    node = node[:]  # pylint: disable=unsubscriptable-object
                else:
                    # Type Guard
                    assert is_node(node)

                    node = copy(node)

                edit_offset = 0
                for ii in range(len(edits)):
                    edit_key = edits[ii][0]
                    edit_value = edits[ii][1]
                    if in_array:
                        # Type Guard
                        assert isinstance(edit_key, int)

                        edit_key -= edit_offset

                    if in_array and edit_value is None:
                        # Type Guard
                        assert isinstance(node, list)
                        assert isinstance(edit_key, int)

                        Array.splice(node, edit_key, 1)
                        edit_offset += 1
                    else:
                        # Type Guard
                        assert isinstance(edit_key, str)
                        assert is_node(node)

                        node[edit_key] = edit_value

            index = stack.index
            keys = stack.keys
            edits = stack.edits
            in_array = stack.in_array
            stack = stack.prev
        else:
            # key = (index if in_array else keys[index]) if parent is not None else None
            if parent is not None:
                if in_array:
                    key = index
                else:
                    # Type Guard
                    assert isinstance(keys[0], str)
                    keys = cast(list[str], keys)

                    key = keys[index]
            else:
                key = None

            # node = parent[key] if parent is not None else new_root
            if parent is not None:
                if isinstance(parent, list):
                    # Type Guard
                    assert isinstance(key, int)

                    node = parent[key]  # pylint: disable=unsubscriptable-object
                else:  # is_node(parent)
                    # Type Guard
                    assert isinstance(key, str)

                    node = parent[key]  # pylint: disable=unsubscriptable-object

            else:
                node = new_root

            if node is None or node is undefined:
                continue
            if parent is not None:
                # Type Guard
                assert key is not None

                path.append(key)

        result: Any = undefined
        if not Array.is_array(node):
            if not is_node(node):
                raise Exception(f'Invalid AST Node: {inspect(node)}.')
            visit_fn = get_visit_fn(visitor, node.kind, is_leaving)
            if visit_fn is not None:
                # Type Guard
                assert parent is not None

                result = visit_fn(visitor, node, key, parent, path, ancestors)

                if result is BREAK:
                    break

                if result is False:
                    if not is_leaving:
                        path.pop()
                        continue
                elif result is not undefined:
                    # Type Guard
                    assert key is not None

                    edits.append((key, result))
                    if not is_leaving:
                        if is_node(result):
                            node = result
                        else:
                            path.pop()
                            continue

        if result is undefined and is_edited:
            # Type Guard
            key = cast(Union[str, int], key)

            edits.append((key, node))

        if is_leaving:
            path.pop()
        else:
            stack = _Stack(in_array=in_array, index=index, keys=keys, edits=edits, prev=stack)
            in_array = Array.is_array(node)
            # keys = node if in_array else query_document_keys.get(node.kind, [])
            if in_array:
                # Type Guard
                assert isinstance(node, list)

                keys = node
            else:
                # Type Guard
                assert is_node(node)

                keys = query_document_keys.get(node.kind, [])

            index = -1
            edits = []
            if parent is not None:
                ancestors.append(parent)
            parent = node

        if stack is None:
            break

    if len(edits) != 0:
        new_root = edits[-1][1]

    return new_root


# ASTVisitor should not be defined here according to graphql-js,
# but confined by Python's syntax, ASTNode can only refer the types defined above,
# so their definition settle down here.

# A visitor is provided to visit, it contains the collection of
# relevant functions to be called during the visitor's traversal.
ASTVisitor = Union[EnterLeaveVisitor[ASTNode], KindVisitor]


def visit_in_parallel(visitors: Sequence[ASTVisitor]) -> ASTVisitor:
    """
    Creates a new visitor instance which delegates to many visitors to run in
    parallel. Each visitor will be visited for each node before moving on.

    If a prior visitor edits a node, no following visitors will see that node.
    """

    skipping: list[Optional[Union[UndefinedType, _BreakType, ASTNode]]] = [None] * len(visitors)

    class _ParallelVisitor(EnterVisitor, LeaveVisitor):
        def enter(self, *args):
            node: Final[ASTNode] = args[0]
            for i in range(len(visitors)):
                if skipping[i] is None:
                    fn = get_visit_fn(visitors[i], node.kind, False)
                    if fn is not None:
                        result = fn(visitors[i], *args)
                        if result is False:
                            skipping[i] = node
                        elif result is BREAK:
                            skipping[i] = BREAK
                        elif result is not undefined:
                            return result

        def leave(self, *args):
            node: Final[ASTNode] = args[0]
            for i in range(len(visitors)):
                if skipping[i] is None:
                    fn = get_visit_fn(visitors[i], node.kind, True)
                    if fn is not None:
                        result = fn(visitors[i], *args)
                        if result is BREAK:
                            skipping[i] = BREAK
                        elif result is not undefined and result is not None:
                            return result

                elif skipping[i] == node:
                    skipping[i] = None

    return _ParallelVisitor()


def get_visit_fn(visitor: ASTVisitor, kind: str, is_leaving: bool) -> Optional[ASTVisitFn[ASTNode]]:
    kind_visitor: Optional[ASTVisitFn[ASTNode] | EnterLeaveVisitor[ASTNode]] = getattr(
        visitor, kind
    )
    if kind_visitor is not None:
        if typeof(kind_visitor) == 'function':
            if is_leaving:
                return None
            else:
                kind_visitor = cast(ASTVisitFn[ASTNode], kind_visitor)
                return kind_visitor

        if is_leaving:
            kind_visitor = cast(EnterVisitor[ASTNode], kind_visitor)
            return kind_visitor.enter
        else:
            kind_visitor = cast(LeaveVisitor[ASTNode], kind_visitor)
            return kind_visitor.leave

    if is_leaving:
        kind_visitor = cast(EnterVisitor[ASTNode], kind_visitor)
        return kind_visitor.enter
    else:
        kind_visitor = cast(LeaveVisitor[ASTNode], kind_visitor)
        return kind_visitor.leave
