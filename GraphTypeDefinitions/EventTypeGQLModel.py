import strawberry
import datetime
from typing import Union, List, Annotated, Optional
from .utils import withInfo, getLoaders

EventGQLModel = Annotated["EventGQLModel", strawberry.lazy(".EventGQLModel")]

@strawberry.federation.type(keys=["id"], description="""Represents an event type""")
class EventTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: strawberry.ID):
        loader = getLoaders(info).eventtypes
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

    @strawberry.field(description="""Related events""")
    async def events(self, info: strawberry.types.Info) -> Optional[List['EventGQLModel']]:
        loader = getLoaders(info).event_eventtype_id
        result = await loader.load(self.id)
        return result

