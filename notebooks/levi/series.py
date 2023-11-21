import pandas as pd
from pandas import DataFrame

import numpy as np
from scipy import sparse

from beartype import beartype
from beartype.vale import IsAttr, IsEqual, IsSubclass, IsInstance
from typing import Annotated

# TODO : use pandas categorical: https://github.com/pandas-dev/pandas/issues/50996

@pd.api.extensions.register_series_accessor("levi")
class LeviAccessor:
    def __init__(self, pandas_obj):
        self._validate(pandas_obj)
        self._obj = pandas_obj

    levi_series = Annotated[pd.Series, 
                               IsInstance[pd.Series] &
                               IsAttr['index', IsInstance[pd.MultiIndex]]
                               ]

    @staticmethod
    @beartype
    def _validate(obj: levi_series):
        print("*** test validator***") 
        # TODO: use beartype
        # if type(obj) is not pd.Series:
        #     raise AttributeError("Must be Levi Graph Representation in MultiIndex Pandas Series format")  #FIXME this is just filler to get accessor to run, need to update

    def to_edgelist(self, level_0: str = "level_0", level_1: str = "level_1") -> DataFrame:
        adj = self._obj.levi.to_adjacency()
        edgelist_df = adj.unstack().reset_index().rename(
            columns={"level_0": level_0, "level_1": level_1, "0": "weight"}) 
            # .astype({i.name:i.dtype for i in (affinity.index,affinity.columns)})
            # TODO: use melt.reset_index like in SURF code?
        return edgelist_df

    def to_adjacency(self, level_0: str = "level_0", level_1: str = "level_1") -> DataFrame:
        # similar to nx.from_pandas_edgelist()
        df = self._obj.to_frame().reset_index()
        A = pd.crosstab(df.iloc[:, 0], df.iloc[:, 1])
        df2 = A.T @ A  #TODO: handle different types of functions  levi.project(on: level_0, function: Callable[leviSeries, df], dot_product)
        np.fill_diagonal(df2.values, 0)
        df2.index.name = None
        return df2

    def to_biadjacency(self) -> DataFrame:
        # FIXME: accommodate full set of possible nodes, even in not in dataset. 
        return self._obj.unstack(level=1, fill_value=0).rename_axis(None, index=0).rename_axis(None, axis=1)

    def to_new_levi(self, level_0="level_0",  level_1="level_1"):
        self._obj.index.names = [None, None]
        levi_df = self._obj.reset_index() #.rename(
            #columns={"level_0": level_0, "level_1": level_1})
        new_levi_df = (pd.concat([levi_df[[level_0, "flag"]], levi_df[[level_1, "flag"]]])
                       .reset_index()
                       .rename(columns={level_1: level_0})
                       .stack()
                       .unstack()
                       )
        new_levi = new_levi_df.set_index(["index", "level_0"]).squeeze()
        return new_levi