import pandas as pd
from pandas import DataFrame

import numpy as np
from scipy import sparse

from beartype import beartype
from beartype.vale import IsAttr, IsEqual, IsSubclass, IsInstance
from typing import Annotated

# TODO : use pandas categorical: https://github.com/pandas-dev/pandas/issues/50996


# can also be df, series, or index
@pd.api.extensions.register_series_accessor("levi")
class LeviAccessor:
    def __init__(self, pandas_obj):
        self._validate(pandas_obj)
        self._obj = pandas_obj

    series_2Dindex = Annotated[pd.Series,  # need this pd.Series?
                               IsInstance[pd.Series] &
                               IsAttr['index', IsInstance[pd.MultiIndex]]
                               ]

    @staticmethod
    @beartype
    def _validate(obj: series_2Dindex):
        print("*** test validator***")
        # TODO: use beartype
        # if type(obj) is not pd.Series:
        #     raise AttributeError("Must be Levi Graph Representation in MultiIndex Pandas Series format")  #FIXME this is just filler to get accessor to run, need to update

    def to_edgelist(self, level_0: str = "level_0", level_1: str = "level_1") -> DataFrame:
        adj = self._obj.levi.to_adjacency()
        edgelist_df = adj.unstack().reset_index().rename(
            columns={"level_0": level_0, "level_1": level_1, "0": "weight"})
        return edgelist_df

    def to_adjacency(self, level_0: str = "level_0", level_1: str = "level_1") -> DataFrame:
        # similar to nx.from_pandas_edgelist()
        df = self._obj.to_frame().reset_index()
        A = pd.crosstab(df[level_0], df[level_1])
        df2 = A.T @ A  #TODO: handle different types of functions  levi.project(on: level_0, function: Callable[leviSeries, df], dot_product)
        np.fill_diagonal(df2.values, 0)
        df2.index.name = None
        return df2

    @property
    def to_biadjacency(self) -> DataFrame:
        # FIXME: accommodate full set of possible nodes, even in not in dataset. Fix extra index in columns: "flag"
        return self._obj.unstack(level=1, fill_value=0)

    @property
    def to_new_levi(self, level_0='level_0',  level_1='level_1'):
        el = self._obj.levi.to_edgelist()
        new_levi_el = (pd.concat([el[[level_0, "flag"]], el[[level_1, "flag"]]])
                       .reset_index()
                       .rename(columns={level_1: level_0})
                       .stack()
                       .unstack()
                       )
        new_levi = new_levi_el.set_index(["index", "level_0"]).squeeze()
        return new_levi