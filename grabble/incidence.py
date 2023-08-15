# from attrs import frozen, evolve, field, define
from dataclasses import dataclass
import static_frame as sf
from bidict import frozenbidict
from functools import cache
from cytoolz import valmap
import beartype.typing as bt
from beartype.vale import IsAttr, IsEqual
from beartype.door import is_bearable

@beartype
@dataclass
class Incidence:
    """triple $(E1, E2, I), I \in E1 \cross E2$  
    we go ahead and store these in `frozenbidict`'s to enable fast lookup of integer IDs 
    """
    entities: bt.Tuple[EntityIndex, EntityIndex]
    flags: sf.Series  # should be Series[IndexHierarchy[E1, E2], int|bool]
    
RoleIndex: bt.TypeAlias = frozenbidict[str, Incidence]


def matrix_from_incidence(inc: Incidence)-> sprs.csc_array:
    """detour through coo_array, using size(entity_set)x2 for shape"""
    row_idx = inc.flags.index.values_at_depth(0)
    col_idx = inc.flags.index.values_at_depth(1)
    shape = tuple(len(bd) for bd in inc.entities)
    return sprs.coo_array((ein, (row_idx, col_idx)), shape=shape).tocsc()

    
def _wrap_incidence_as_role(inc:Incidence|RoleIndex)->RoleIndex:
    if isinstance(inc, Incidence):
        return frozencbidict(base=inc)
    else: 
        return inc 

def _get_base_or_first(d, basename):
    return d.get(basename, d[next(iter(d))])

@frozen 
class Levi:
    # flags: sf.Series  # Series[IndexHierarchy[E1, E2], int|bool]
    role_flags:RoleIndex=field(converter=_wrap_incidence_as_role) 
    # ^ Different possible roles to play in an incidence structure
    base_name:str = 'base'  # the name of the role that we use by default

    # ^ should auto-gen a default "base" if not provided
    # entity_sets: bt.Tuple[bt.Set, bt.Set]  # O(1) membership tests, not index-construction
    # ^ probably better as bidict to enable int/pos <--> name by default. 
    # B: sprs.csc_array = field()
    
    @property
    def flags(self)->sf.Series:
        return _get_base_or_first(self.role_flags,self.base).flags
    
    @cache
    @property
    def roles(self)-> bt.Mapping[str, sprs.csc_array]:
        return valmap(self.role_flags, matrix_from_incidence)
                      
    @property
    def B(self)->sprs.csc_array:
        return _get_base_or_first(self.roles, self.base)
    
@define
class Grabble:
    """rank-N incidence structure, used for multiway analysis and
    promotion of columnar types to entities with their own incidences"""

# @define        
# class Grabble:
#