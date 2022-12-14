from attrs import frozen, evolve, field, define
import static_frame as sf
import numpy as np
from bidict import frozenbidict
from functools import cache
from cytoolz import valmap
import beartype.typing as bt
from beartype.vale import IsAttr, IsEqual, IsInstance, Is
from beartype.door import is_bearable

FlagDType = bt.TypeVar('FlagDType', bound=bt.Hashable)
EntityKind = bt.TypeVar('EntityKind', bound=str) # should be PEP675 `LiteralString`
EntityIndex: bt.TypeAlias = frozenbidict[FlagDType,int]

def IsBearable(beartype:bt.Type):
    return Is[lambda instance: is_bearable(instance, beartype)]
# FlagsIndexType:bt.TypeAlias = bt.Callable[s
def FlagsIndex(t1: EntityKind, t2: EntityKind)->bt.Type[sf.IndexHierarchy]:
    # change to __beartype_hint__ system in the future

    # def __class_getitem__(cls, cross: bt.Tuple[EntityKind, EntityKind])-> bt.Any:
    
    return bt.Annotated[
        sf.IndexHierarchy,
        # object, 
        # IsInstance[sf.SeriesHE]
        IsAttr['name', IsEqual[(t1, t2)]]
        & IsAttr['depth', IsEqual[2]]
    ]

def RoleFlags(t1:EntityKind, t2:EntityKind, role:str='base', flag_value_type:bt.Type=np.dtype.int64)->bt.Type[sf.SeriesHE]:
    return bt.Annotated[
        sf.SeriesHE,
        IsAttr['index', IsBearable(FlagsIndex(t1,t2))]
        &
        IsAttr['dtypes',IsEqual[flag_value_type]]
        &
        IsAttr['name', IsEqual[role]
    ]
    

    
