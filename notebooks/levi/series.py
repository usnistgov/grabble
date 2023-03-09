import pandas as pd
from pandas import DataFrame

import numpy as np
from scipy import sparse

@pd.api.extensions.register_series_accessor("levi")   #can also be df, series, or index
class LeviAccessor:
    def __init__(self, pandas_obj):
        self._validate(pandas_obj)
        self._obj = pandas_obj

    @staticmethod
    def _validate(obj):
        # TODO: use beartype
        if type(obj) is not pd.Series:
            raise AttributeError("Must be Levi Graph Representation in MultiIndex Pandas Series format")  #FIXME this is just filler to get accessor to run, need to update
        

    def to_edgelist(self, level_0="level_0", level_1="level_1"):
        edgelist_df = self._obj.reset_index().rename(columns={"level_0": level_0, "level_1": level_1})
        return edgelist_df
    
    @property
    def to_adjacency(self, level_0="level_0", level_1="level_1"):
        # similar to nx.from_pandas_edgelist()
        # TODO: handle different names for level_0, level_1
        df = self._obj.to_frame().reset_index()
        A = pd.crosstab(df.level_0, df.level_1)
        df2 = A.T @ A
        np.fill_diagonal(df2.values, 0)
        df2.index.name = None
        return df2
    
    @property
    def to_biadjacency(self):
        # FIXME: accommodate full set of possible nodes, even in not in dataset. Fix extra index in columns: "flag"
        return self._obj.unstack(level=1, fill_value=0)
    

    # Reevaluate the following methods? They are taking other input and not really accessors of original levi graph
    # For now, copied in relevant code from SURF repo, to be adapted

    def biadjacency_to_edgelist(self, biadjacency, value_name='weight'):
        # TODO
        # return (biadjacency.melt(ignore_index=False, value_name=value_name)
        #   .reset_index().astype(dict(((i.name), (i.dtype)) for i in (biadjacency.index, biadjacency.columns))))
        return self
    
    def edgelist_to_biadjacency(self, edgelist, source_name, target_name, value_name='weight'):
        # TODO
        #return (edgelist.pivot(index=source_name, columns=target_name, values=value_name)
        #   .reindex(columns=edgelist[target_name].unique(), index=edgelist[source_name].unique()).astype(float).fillna(0))
        return self

    def edgelist_to_incidence(self, edgelist, node_colname, value_colname=None):
        #TODO
        # """assume edgelist is indexed by edge number, not some edge set of names (for now)"""
        # data = np.ones_like(edgelist.index.values) if value_colname == None else edgelist[value_colname].values
        # return sparse.coo_array((data, (edgelist.index, edgelist[node_colname].cat.codes)), shape=(edgelist.shape[0], len(edgelist[node_colname].cat.categories))) 
        return self
    
    def edgelist_to_bipartite(self, edgelist):
        # TODO - similar to edge_to_bp in SURF code, but want pandas format output, not networkx graph
        return self


    
    
    
    
    