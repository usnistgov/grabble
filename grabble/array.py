import numpy as np
import pandas as pd
from pandas.api.extensions import (
    ExtensionArray,
    ExtensionDtype,
    register_extension_dtype,
    ExtensionScalarOpsMixin,
)
from typing import FrozenSet, Iterable, TypeVar, Tuple
from .base import BaseEdge, DirectedEdge

T = TypeVar("T")


class GraphEdgeDtype(ExtensionDtype):
    type = BaseEdge
    name = "graph_edges"
    na_value = np.nan


class DirectedEdgeDtype(ExtensionDtype):
    type = DirectedEdge
    name = "directed_edges"
    na_value = np.nan


register_extension_dtype(GraphEdgeDtype)
register_extension_dtype(DirectedEdgeDtype)


class GraphEdgeArray(ExtensionArray, ExtensionScalarOpsMixin):
    _dtype = GraphEdgeDtype()

    def __init__(
        self,
        data,
    ):
        if isinstance(data, self.__class__):
            data = data.data

        elif not isinstance(data, np.ndarray):
            raise TypeError(
                "'data' should be array of source,target pairs. Use from_edgelist, "
                "from_nodearrays functions to construct a GraphEdgeArray."
            )
        elif not data.ndim == 1:
            raise ValueError(
                "'data' should be a 1-dimensional array of source-target pairs."
            )
        self.data = data

    @classmethod
    def from_edgelist(cls, edges=Iterable[Tuple[T, T]]):

        if isinstance(edges, BaseEdge):
            edges = [edges]
        out = np.empty(len(edges), dtype=object)
        out[:] = [BaseEdge(e) for e in edges]
        return out

    @property
    def dtype(self):
        return self._dtype


GraphEdgeArray._add_arithmetic_ops()
GraphEdgeArray._add_comparison_ops()


class DirectedEdgeArray(ExtensionArray):
    _dtype = DirectedEdgeDtype()

    @property
    def dtype(self):
        return self._dtype

    # def __init__(self, data):
