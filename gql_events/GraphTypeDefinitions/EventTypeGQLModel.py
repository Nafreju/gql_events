import strawberry as strawberryA
import datetime
from typing import Union, List, Annotated, Optional
from .utils import withInfo, getLoaders
from ..GraphResolvers import resolveGroupsForEvent, resolvePresencesForEvent

EventGQLModel = Annotated["EventGQLModel", strawberryA.lazy(".EventGQLModel")]

@strawberryA.federation.type(keys=["id"], description="""Represents an event type""")
class EventTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).eventtypes
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Name of type (cze)""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Name of type (en)""")
    def name_en(self) -> str:
        return self.name_en

    @strawberryA.field(description="""Related events""")
    async def events(self, info: strawberryA.types.Info) -> Optional[List['EventGQLModel']]:
        loader = getLoaders(info).event_eventtype_id
        result = await loader.load(self.id)
        return result

