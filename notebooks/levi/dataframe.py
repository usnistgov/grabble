import pandas as pd
from pandas import DataFrame
# from pandas.api.extenstions import register_dataframe_accessor

# from levi import ACCESSOR_NAME

@pd.api.extensions.register_dataframe_accessor("levi")   #can also be df, series, or index
class LeviAccessor:
    def __init__(self, pandas_obj):
        self._validate(pandas_obj)
        self._obj = pandas_obj

    @staticmethod
    def _validate(obj):
        # TODO: use beartype
        if type(obj) is not pd.DataFrame:
            raise AttributeError("Must be cooccurrence Dataframe")  #FIXME this is just filler to get accesor to run, need to update
        

    @property
    def from_dataframe(self):
        test = self._obj()
        return 

    @property
    def test_attr(self):        
        return self._obj.iloc[0]
    
    @property
    def incidence_matrix(self):
        return self._obj.unstack(level=1, fill_value=0)
    
    
    