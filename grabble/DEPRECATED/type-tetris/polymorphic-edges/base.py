# from collections.abc import Set, Hashable
from typing import NamedTuple, TypeVar, Union, List, Tuple, Optional

T = TypeVar("T")
# NodeContainer = Union[List, FrozenSet, Tuple]
NodeContainer = Tuple[T, T]


class DirectedEdge(NamedTuple):
    source: object
    target: object


# class BaseEdge(DirectedEdge):
#     def __new__(cls, data):
#         return frozenset()
# class BaseEdge(FrozenSet):
#     # TODO: Should be limited to 2-ary frozenset (someday hypergraph?)
#     def __init__(self, nodes: NodeContainer, *args, **kwgs):
#         super(BaseEdge, self).__init__(nodes, *args, **kwgs)


# class BaseEdge(Set, Hashable):
#     """An example of a custom frozenset-like object using
#     Abstract Base Classes.
#     from (stackoverflow user bjmc)[https://stackoverflow.com/a/6698723]
#     """

#     __hash__ = Set._hash

#     wrapped_methods = (
#         "difference",
#         "intersection",
#         "symetric_difference",
#         "union",
#         "copy",
#     )

#     def __repr__(self):
#         return "BaseEdge({0})".format(list(self._set))

#     def __new__(cls, iterable: Optional[NodeContainer] = None):
#         selfobj = super(BaseEdge, cls).__new__(BaseEdge)
#         selfobj._set = frozenset() if iterable is None else frozenset(iterable)
#         for method_name in cls.wrapped_methods:
#             setattr(selfobj, method_name, cls._wrap_method(method_name, selfobj))
#         return selfobj

#     @classmethod
#     def _wrap_method(cls, method_name, obj):
#         def method(*args, **kwargs):
#             result = getattr(obj._set, method_name)(*args, **kwargs)
#             return BaseEdge(result)

#         return method

#     def __getattr__(self, attr):
#         """Make sure that we get things like issuperset() that aren't provided
#         by the mix-in, but don't need to return a new set."""
#         return getattr(self._set, attr)

#     def __contains__(self, item):
#         return item in self._set

#     def __len__(self):
#         return len(self._set)

#     def __iter__(self):
#         return iter(self._set)
