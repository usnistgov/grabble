""" Top-level Levi Graph package (Levi pandas accessor)"""

import logging
from logging import NullHandler

logging.getLogger(__name__).addHandler(NullHandler())

# ACCESSOR_NAME = 'levi'

from .dataframe import LeviAccessor

# from tqdm.autonotebook import tqdm
from tqdm.auto import tqdm
tqdm.pandas()
