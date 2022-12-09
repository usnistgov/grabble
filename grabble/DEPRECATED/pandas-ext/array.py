import numpy as np
import pandas as pd
from pandas.api.extensions import (
    ExtensionArray,
    ExtensionDtype,
    register_extension_dtype,
    ExtensionScalarOpsMixin,
)
from typing import FrozenSet, Iterable, TypeVar, Tuple, List, Set, Union, Type
from .base import DirectedEdge, NodeContainer

T = TypeVar("T")
EdgeList = Iterable[NodeContainer]


@register_extension_dtype
class GraphEdgeDtype(ExtensionDtype):
    @property
    def type(self):
        return frozenset

    @property
    def name(self) -> str:
        return "GraphEdgeDtype"

    @property
    def na_value(self) -> object:
        return np.nan

    @classmethod
    def construct_from_string(cls, s: str):
        return _construct_from_string(cls, s)

    @classmethod
    def construct_array_type(cls):
        return GraphEdgeArray


@register_extension_dtype
class DirectedEdgeDtype(ExtensionDtype):
    @property
    def type(self):
        return DirectedEdge

    @property
    def name(self) -> str:
        return "DirectedEdgeDtype"

    @property
    def na_value(self) -> object:
        return np.nan

    @classmethod
    def construct_from_string(cls, s: str):
        return _construct_from_string(cls, str)

    @classmethod
    def construct_array_type(cls):
        return DirectedEdgeArray


class GraphEdgeArray(ExtensionArray, ExtensionScalarOpsMixin):
    def __init__(self, data):
        self.data = _check_array_data(self, data)

    @classmethod
    def from_edgelist(cls, edges: EdgeList):
        arr = _construct_array_vectorized(frozenset, edges)
        return GraphEdgeArray(arr)

    @property
    def dtype(self) -> ExtensionDtype:
        return GraphEdgeDtype()

    @property
    def as_directed(self):
        # TODO: add ability to custom sort (key, etc.)
        return DirectedEdgeArray.from_edgelist(self.tolist())


GraphEdgeArray._add_arithmetic_ops()
GraphEdgeArray._add_comparison_ops()


class DirectedEdgeArray(ExtensionArray, ExtensionScalarOpsMixin):
    def __init__(self, data):
        self.data = _check_array_data(self, data)

    @classmethod
    def from_edgelist(cls, edges: EdgeList):
        arr = _construct_array_vectorized(DirectedEdge, edges)
        return DirectedEdgeArray(arr)

    @property
    def as_undirected(self):
        return GraphEdgeArray.from_edgelist(self.tolist())

    @property
    def dtype(self) -> ExtensionDtype:
        return DirectedEdgeDtype()

    # def __init__(self, data):


GraphEdgeArrayType = Union[GraphEdgeArray, DirectedEdgeArray]


def _construct_from_string(cls, string):
    """temporary usage from geopandas"""
    if not isinstance(string, str):
        raise TypeError(
            "'construct_from_string' expects a string, got {}".format(type(string))
        )
    elif string == cls.name:
        return cls()
    else:
        raise TypeError(
            "Cannot construct a '{}' from '{}'".format(cls.__name__, string)
        )


def _check_array_data(cls: Type[ExtensionArray], data):
    if isinstance(data, cls.__class__):
        data = data.data

    elif not isinstance(data, np.ndarray):
        raise TypeError(
            "'data' should be array. Use `from_X`"
            "functions to construct a this array type from supported data."
        )
    elif not data.ndim == 1:
        raise ValueError("'data' should be a 1-dimensional array of values.")
    return data


def _construct_array_vectorized(arr_type: T, data: Union[T, Iterable[T]]):
    if isinstance(data, arr_type):
        data = [data]
    out = np.empty(len(data), dtype=object)
    out[:] = [arr_type(d) for d in data]
    return out


def _from_edgelist(edge_type: Type[GraphEdgeArrayType], edges: EdgeList):
    """More specific version of array construction with type annotations"""
    return _construct_array_vectorized(edge_type, edges)
