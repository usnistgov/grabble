from __future__ import annotations
import pandas as pd
from typing import Mapping, Union
from enum import Enum

# ways we support building a GrabbleFrame's component DataFrames
FrameConstruct = Union[pd.DataFrame, Mapping]


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

        def get_pos(arg):
            try:
                idx = list(cls).index(arg)
            except ValueError:
                vals = [i.value for i in cls]
                idx = vals.index(arg)
            return idx

        idx = get_pos(arg)
        assert (
            len(options) >= idx
        ), "THE DESIRED TYPE IS TOO LOW-PRIORITY (pass more options)!"
        assert len(options) <= len(cls), "TOO MANY OPTIONS SUPPLIED!"

        return options[idx]


def _parse_frameconstruct(frame: FrameConstruct) -> pd.DataFrame:
    """Helper function to allow optionally passing frame constituents (when not built already)"""
    if isinstance(frame, pd.DataFrame):
        return frame
    else:
        return pd.DataFrame(**frame)


class GrabbleFrame(pd.DataFrame):
    """Custom Subclass of pandas.DataFrame for "tidy" graph/network data

    see example for design pattern,
    [here](https://github.com/pandas-dev/pandas/issues/19300#issuecomment-358739959).
    """

    # __doc__ += pd.DataFrame.__doc__
    # ORIGINAL WAY USING DATAFRAME EXTENSION/SUBCLASSING
    #     # temporary properties
    #     _internal_names = pd.DataFrame._internal_names + ["internal_cache"]
    #     _internal_names_set = set(_internal_names)

    # def __new__(  # THE HACK USING EXTRA ATTRIBUTES ON AN ACTUAL DATAFRAME
    #     cls,
    #     nodeframe,  #: FrameConstruct,
    #     edgeframe,  #: FrameConstruct,
    #     active: GraphFrameTypes = GraphFrameTypes.default(),
    # ):
    #     """Create a new node/edge dataframe and it's counterpart

    #     Can either pass an existing set of frames, or a mapping with keyword arguments
    #     to pass to the underlying `pandas.DataFrame` constructor.
    #     """
    #     frame = GraphFrameTypes.pick_option(active, nodeframe, edgeframe)
    #     return super().__new__(cls, frame)
    @property
    def _constructor(self):
        return GrabbleFrame._internal_ctor

    _metadata = ["nodes", "edges", "active"]

    @classmethod
    def _internal_ctor(cls, *args, **kwargs):
        kwargs["nodes"] = None
        kwargs["edges"] = None
        kwargs["active"] = None
        return cls(*args, **kwargs)

    def __init__(
        self,
        nodes_data,
        edges_data,
        # nodeframe: FrameConstruct,
        # edgeframe: FrameConstruct,
        active: GraphFrameTypes = GraphFrameTypes.default(),
        index=None,
        columns=None,
        dtype=None,
        copy=None,
    ):
        """Initialize the grabble with cached node and edge frames.

        The currently `active` frame is usable directly with pandas methods (e.g. chaining)

        """
        data = GraphFrameTypes.pick_option(active, nodes_data, edges_data)

        super(GrabbleFrame, self).__init__(
            data=data, index=index, columns=columns, dtype=dtype, copy=copy
        )
        self.nodes = nodes_data
        self.edges = edges_data
        self.active = active

    # @property
    # def nodes(self) -> pd.DataFrame:
    #     return self._nodes

    # @property
    # def edges(self) -> pd.DataFrame:
    #     return self._edges

    # @property
    # def active(self) -> GraphFrameTypes:
    #     return self._active

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

    # @property
    # def _constructor_sliced(self):
    #     return SubclassedSeries
