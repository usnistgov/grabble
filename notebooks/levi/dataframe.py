import pandas as pd
from pandas import DataFrame

import numpy as np
from scipy import sparse

#TODO : use pandas categorical: https://github.com/pandas-dev/pandas/issues/50996

@pd.api.extensions.register_dataframe_accessor("levi")   #can also be df, series, or index
class LeviAccessor:
    def __init__(self, pandas_obj):
        self._validate(pandas_obj)
        self._obj = pandas_obj

    @staticmethod
    def _validate(obj):
        # TODO: use beartype
        if type(obj) is not pd.DataFrame:
            raise AttributeError("Must be Levi Graph Representation")  #FIXME this is just filler to get accessor to run, need to update
        

    # @property
    # def to_edgelist(self, level_0="level_0", level_1="level_1"):
    #     # TODO
    #     return self.reset_index().rename(columns={"level_0": level_0, "level_1": level_1})
    
    # @property
    # def to_adjacency(self):
    #     # TODO
    #     return self
    
    # @property
    # def to_biadjacency(self):
    #     # FIXME: accommodate full set of possible nodes, even in not in dataset. Fix extra index in columns: "flag"
    #     return self._obj.unstack(level=1, fill_value=0)
    

    
    # For now, copied in relevant code from SURF repo, to be adapted

    def biadjacency_to_edgelist(self, biadjacency, value_name='weight'):
        # TODO
        # return (biadjacency.melt(ignore_index=False, value_name=value_name)
        #   .reset_index().astype(dict(((i.name), (i.dtype)) for i in (biadjacency.index, biadjacency.columns))))
        return self
    
    def edgelist_to_biadjacency(self, source_name, target_name, value_name='weight'):
        # TODO
        return (self.pivot(index=source_name, columns=target_name, values=value_name)
          .reindex(columns=self[target_name].unique(), index=edgelist[source_name].unique()).astype(float).fillna(0))
        # return self

    def edgelist_to_incidence(self, edgelist, node_colname, value_colname=None):
        #TODO
        # """assume edgelist is indexed by edge number, not some edge set of names (for now)"""
        # data = np.ones_like(edgelist.index.values) if value_colname == None else edgelist[value_colname].values
        # return sparse.coo_array((data, (edgelist.index, edgelist[node_colname].cat.codes)), shape=(edgelist.shape[0], len(edgelist[node_colname].cat.categories))) 
        return self
    
    def edgelist_to_bipartite(self, edgelist):
        # TODO - similar to edge_to_bp in SURF code, but want pandas format output, not networkx graph
        return self


    
    
    
    
    