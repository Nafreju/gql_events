import strawberry
import datetime
from typing import Union, List, Annotated, Optional
from .utils import withInfo, getLoaders
from ..GraphResolvers import resolveGroupsForEvent, resolvePresencesForEvent


@strawberry.federation.type(keys=["id"], description="""Represents a type of presence (like Present)""")
class PresenceTypeGQLModel:

    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: strawberry.ID):
        loader = getLoaders(info).presencetypes
        if id is None:
            return None
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberry.field(description="""Primary key""")
    def id(self) -> strawberry.ID:
        return self.id

    @strawberry.field(description="""Name of type (cze)""")
    def name(self) -> str:
        return self.name

    @strawberry.field(description="""Name of type (en)""")
    def name_en(self) -> str:
        return self.name_en
