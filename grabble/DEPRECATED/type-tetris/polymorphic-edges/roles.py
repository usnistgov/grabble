from enum import Enum
from typing import Literal
from phantom import Phantom
from phantom.predicates.generic import identical

class RelatedRole(str, Phantom, predicate=identical('related')):
    ...


class EdgeRoles(Enum):
    """Classical role definitions for simple graphs

    Implemented as an `enum.Flag` to allow the treatment of undirected
    edges as a combination of being both SOURCE and TARGET, as they would
    be represented in e.g. an adjacency matrix.
    """

    SOURCE = "source"
    TARGET = "target"


class PredicateRoles(Enum):
    """Role definitions for SVO/RDF-style edges"""

    SUBJECT = "subject"
    OBJECT = "object"
