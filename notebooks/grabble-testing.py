# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:hydrogen
#     text_representation:
#       extension: .py
#       format_name: hydrogen
#       format_version: '1.3'
#       jupytext_version: 1.11.3
#   kernelspec:
#     display_name: Python [conda env:nestor-dev]
#     language: python
#     name: conda-env-nestor-dev-py
# ---

# %%
import re
import requests
from pathlib import Path
import tqdm.autonotebook as tqdm

import pandas as pd
import numpy as np
import toolz.curried as tz
from toolz.sandbox.core import unzip
import deepgraph as dg
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline

from nestor.datasets import load_excavators
from scipy.sparse import load_npz, csr_matrix, linalg
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS


# %%
class Grabble(pd.DataFrame):

    # temporary properties
    _internal_names = pd.DataFrame._internal_names + ["internal_cache"]
    _internal_names_set = set(_internal_names)

    # normal properties
    _metadata = ["added_property"]

    @property
    def _constructor(self):
        return SubclassedDataFrame2
    
        @property
    def _constructor_sliced(self):
        return SubclassedSeries
