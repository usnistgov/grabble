from typing import Iterator, Mapping, NamedTuple


class DirectedEdge(NamedTuple):
    source: object
    target: object


class BaseEdge(frozenset):
    # TODO: Should be limited to 2-ary frozenset (someday hypergraph?)
    pass
