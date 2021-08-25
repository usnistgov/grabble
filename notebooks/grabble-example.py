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
#     display_name: Python [conda env:grabble]
#     language: python
#     name: conda-env-grabble-py
# ---

# %%
%load_ext autoreload
%autoreload 2

# %%
# import re
# import requests
from pathlib import Path
# import tqdm.autonotebook as tqdm

import pandas as pd
import numpy as np
# import toolz.curried as tz
# from toolz.sandbox.core import unzip
import deepgraph as dg
# import matplotlib.pyplot as plt
# import seaborn as sns
# %matplotlib inline


import grabble as pdg
# from nestor.datasets import load_excavators
# from scipy.sparse import load_npz, csr_matrix, linalg
# from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

# %%
pdg.GrabbleFrame

