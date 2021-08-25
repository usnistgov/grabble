import numpy as np
import pandas as pd
from pandas.api.extensions import (
    ExtensionArray,
    ExtensionDtype,
    register_extension_dtype,
)


class GraphEdgeDtype(ExtensionDtype):
    type = BaseEdges
    name = "graph_edges"
    na_value = np.nan

    @classmethod
    def construct_array_type(cls):
        return GraphEdgeArray


class GraphEdgeArray(ExtensionArray):
    _dtype = GraphEdgeDtype()

    # def __init__(self, data):
