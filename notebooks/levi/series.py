import pandas as pd
from pandas import DataFrame

import numpy as np
from scipy import sparse

from beartype import beartype
from beartype.vale import IsAttr, IsEqual, IsSubclass, IsInstance
from typing import Annotated  

#TODO : use pandas categorical: https://github.com/pandas-dev/pandas/issues/50996

@pd.api.extensions.register_series_accessor("levi")   #can also be df, series, or index
class LeviAccessor:
    def __init__(self, pandas_obj):
        self._validate(pandas_obj)
        self._obj = pandas_obj

    series_2Dindex = Annotated[pd.Series, # need this Series?
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
        # TODO: able to rename "flag" column
        edgelist_df = self._obj.reset_index().rename(columns={"level_0": level_0, "level_1": level_1})
        return edgelist_df
    
    @property
    def to_adjacency(self, level_0: str = "level_0", level_1: str = "level_1") -> DataFrame:
        # similar to nx.from_pandas_edgelist()
        # TODO: handle different names for level_0, level_1
        df = self._obj.to_frame().reset_index()
        A = pd.crosstab(df.level_0, df.level_1)
        df2 = A.T @ A
        np.fill_diagonal(df2.values, 0)
        df2.index.name = None
        return df2
    
    @property
    def to_biadjacency(self) -> DataFrame:
        # FIXME: accommodate full set of possible nodes, even in not in dataset. Fix extra index in columns: "flag"
        return self._obj.unstack(level=1, fill_value=0)
    

    # Reevaluate the flocation of the following methods
    # They should all use Levi series as intermediate step, want to keep catagoricals preserved
    # Commented code is from SURF matchibng code, can be used as starting point

    # def biadjacency_to_edgelist(self, biadjacency: DataFrame, value_name: str = 'weight') -> DataFrame:
    #     # TODO
    #     # return (biadjacency.melt(ignore_index=False, value_name=value_name)
    #     #   .reset_index().astype(dict(((i.name), (i.dtype)) for i in (biadjacency.index, biadjacency.columns))))
    #     return self
    
    # def edgelist_to_biadjacency(self, edgelist: DataFrame, source_name: str, target_name: str, value_name: str = 'weight') -> DataFrame:
    #     # TODO
    #     #return (edgelist.pivot(index=source_name, columns=target_name, values=value_name)
    #     #   .reindex(columns=edgelist[target_name].unique(), index=edgelist[source_name].unique()).astype(float).fillna(0))
    #     return self

    # def edgelist_to_incidence(self, edgelist: DataFrame, node_colname: str, value_colname: str = None) -> DataFrame:
    #     #TODO
    #     # """assume edgelist is indexed by edge number, not some edge set of names (for now)"""
    #     # data = np.ones_like(edgelist.index.values) if value_colname == None else edgelist[value_colname].values
    #     # return sparse.coo_array((data, (edgelist.index, edgelist[node_colname].cat.codes)), shape=(edgelist.shape[0], len(edgelist[node_colname].cat.categories))) 
    #     return self
    
    # def edgelist_to_bipartite(self, edgelis: DataFrame):
    #     # TODO - similar to edge_to_bp in SURF code, but want pandas format output, not networkx graph
    #     return self


    
    
    