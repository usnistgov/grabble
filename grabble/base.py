from typing import FrozenSet, NamedTuple, TypeVar, Union, List, Tuple

T = TypeVar("T")
# NodeContainer = Union[List, FrozenSet, Tuple]
NodeContainer = Tuple[T, T]


class DirectedEdge(NamedTuple):
    source: object
    target: object


class BaseEdge(FrozenSet):
    # TODO: Should be limited to 2-ary frozenset (someday hypergraph?)
    def __init__(self, nodes: NodeContainer, *args, **kwgs):
        super(BaseEdge, self).__init__(nodes, *args, **kwgs)
