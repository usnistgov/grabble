from __future__ import annotations
import pandas as pd
from typing import Mapping
from enum import Enum


class FrameConstruct(Union[pd.DataFrame, Mapping]):
    """ways we support building a GrabbleFrame's component DataFrames"""

    pass


class GraphFrameTypes(Enum):
    """Keeping track of *types* of graph dataframes

    Possible to extend with other kinds, or improve the interface
    with proper typing. Now we can "check equality" with this wrapper
    and change the underlying object later.
    """

    nodes = "nodes"
    edges = "edges"  # TODO: do I want a specific "EdgeFrame"? A pandera.Schema?

    @classmethod
    def default(cls):
        """what frame should be treated as default"""
        return cls.nodes

    @classmethod
    def pick_option(cls, arg: GraphFrameTypes, *options):
        """helper function to select from several options based on a GFT instance"""
        assert (len(options) <= len(cls), "TOO MANY OPTIONS SUPPLIED!")
        return options[list(cls).index(arg)]


def _parse_frameconstruct(frame: FrameConstruct) -> pd.DataFrame:
    """Helper function to allow optionally passing frame constituents (when not built already)"""
    if isinstance(frame, pd.DataFrame):
        return frame
    else:
        return pd.DataFrame(**frame)


class GrabbleFrame(pd.DataFrame):

    # ORIGINAL WAY USING DATAFRAME EXTENSION/SUBCLASSING
    #     # temporary properties
    #     _internal_names = pd.DataFrame._internal_names + ["internal_cache"]
    #     _internal_names_set = set(_internal_names)

    # normal properties
    _metadata = ["nodes", "edges", "active"]

    #     @property
    #     def _constructor(self):
    #         return SubclassedDataFrame2

    #     @property
    #     def _constructor_sliced(self):
    #         return SubclassedSeries

    def __new__(  # THE HACK USING EXTRA ATTRIBUTES ON AN ACTUAL DATAFRAME
        cls,
        nodeframe: FrameConstruct,
        edgeframe: FrameConstruct,
        active: GraphFrameTypes = GraphFrameTypes.default(),
    ):
        """Create a new node/edge dataframe and it's counterpart

        Can either pass an existing set of frames, or a mapping with keyword arguments
        to pass to the underlying `pandas.DataFrame` constructor.
        """
        frame = GraphFrameTypes.pick_option(active, nodeframe, edgeframe)
        return super(GrabbleFrame, cls).__new__(cls, frame)

    def __init__(
        self,
        nodeframe: FrameConstruct,
        edgeframe: FrameConstruct,
        active: GraphFrameTypes = GraphFrameTypes.default(),
    ):
        """Initialize the grabble with cached node and edge frames.

        The currently `active` frame is usable directly with pandas methods (e.g. chaining)

        """
        self._nodes = nodeframe
        self._edges = edgeframe
        self._active = active

    @property
    def nodes(self) -> pd.DataFrame:
        return self._nodes

    @property
    def edges(self) -> pd.DataFrame:
        return self._edges

    @property
    def active(self) -> GraphFrameTypes:
        return self._active

    def activate(self, frametype: GraphFrameType) -> GrabbleFrame:
        """returns a `GrabbleFrame` with a different active component

        Currently assumes immutable grabbleframes, so we don't swap "active" using state.
        This encourages method chaining for now, but eventually should allow stateful mutation
        for imperative style as users probably want that?
        """
        if frametype == self.active:
            return self
        else:
            return GrabbleFrame(self.nodes, self.edges, active=frametype)
