from __future__ import annotations
import typing as t
from typing_extensions import final, Annotated
from classes import AssociatedType, typeclass
from pydantic.generics import GenericModel
import pydantic as pdt

# from phantom import Phantom
# from phantom.predicates import generic, Predicate  # is_bearable?
from beartype import cave

# from beartype.abby import is_bearable
# from functools import partial

from .roles import RelatedRole, EdgeRoles, PredicateRoles
from .base import DirectedBool

# class EnumType(t.Type[Enum], Phantom, predicate=generic.of_type(Enum)):
# ...


RolesOrRelated = cave.EnumType | RelatedRole

# E = t.TypeVar("E", bound=cave.EnumMemberType)
ET = t.TypeVar("ET", bound=RolesOrRelated, covariant=True)


# class Roles(GenericModel, t.Generic[ET]):
#     __root__: t.Dict[str, ET]

#     def __iter__(self):
#         return iter(self.__root__)

#     def __getitem__(self, item):
#         return self.__root__[item]

class Relation(GenericModel, t.Generic[ET]):
    """Generic model of relations in a graph

    Parameterized by a user-defined `enum.Enum` of roles
    to allow flexible role definition and attribute casting
    during validation and parsing.
    """

    id: str | None = None
    roles: t.Dict[str, ET] | None = None
    relation: str | None = None
    label: str | None = None
    metadata: t.Mapping[str, t.Any] | None

    @pdt.validator("roles", each_item=True)
    def _roles_are_membertypes(cls, v):
        _, value = v
        assert isinstance(value, cave.EnumMemberType)
        return v
    class Config:
        use_enum_values = True





@final
class ToRelation(AssociatedType):
    ...


@typeclass(ToRelation)
def to_relation(instance: RolesOrRelated, **data_kws) -> Relation:
    ...


class UndirectedEdge(Relation[RelatedRole]):
    directed: t.Literal[False] | None = False
    source: str
    target: str


class DirectedEdge(Relation[EdgeRoles]):
    directed: t.Literal[True]
    source: str
    target: str


# Can also be written with a custom root type
# class Edge(pdt.BaseModel):
#     __root__ = Annotated[t.Union[UndirectedEdge, DirectedEdge], pdt.Field(discriminator='directed')]

Edge = Annotated[UndirectedEdge | DirectedEdge, pdt.Field(discriminator="directed")]


# @to_relation.instance(t.Type[RelatedRole])
# @to_relation.instance(t.Type[EdgeRoles])
# def _to_edgerelation(instance: EdgeRoles, **data_kws) -> Edge:
#     return pdt.parse_obj_as(Edge, data_kws)


class PredicateRelation(Relation[PredicateRoles]):
    SUBJECT: str
    OBJECT: str


# @to_relation.instance(t.Type[PredicateRoles])
# def _to_predicaterelation(instance: EdgeRoles, **data_kws) -> PredicateRelation:
#     return PredicateRelation(**data_kws)
