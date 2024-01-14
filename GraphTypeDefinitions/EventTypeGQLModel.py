import strawberry
import datetime
from typing import List, Annotated, Optional
from ._GraphResolvers import asPage
from utils import getLoadersFromInfo, getUserFromInfo
from uuid import UUID
from dataclasses import dataclass
from uoishelpers.resolvers import createInputs
from .BaseGQLModel import BaseGQLModel
from GraphTypeDefinitions._GraphResolvers import (
    resolve_id,
    resolve_name,
    resolve_name_en,
    resolve_changedby,
    resolve_created,
    resolve_lastchange,
    resolve_createdby,
    resolve_rbacobject,
    asPage
)
from ._GraphPermissions import OnlyForAuthentized

EventGQLModel = Annotated["EventGQLModel", strawberry.lazy(".EventGQLModel")]
EventCategoryGQLModel = Annotated["EventCategoryGQLModel", strawberry.lazy(".EventCategoryGQLModel")]


@strawberry.federation.type(
    keys=["id"], description="""Represents an event type""")
class EventTypeGQLModel(BaseGQLModel):
    
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).eventtypes

    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en
    
    @strawberry.field(description="""Validity of event type""",
        permission_classes=[OnlyForAuthentized()])
    def valid(self) -> Optional[bool]:
        return self.valid
    
    created = resolve_created
    lastchange = resolve_lastchange
    createdby = resolve_createdby
    changedby = resolve_changedby
    
    @strawberry.field(description="""Category id of event type""",
        permission_classes=[OnlyForAuthentized()])
    def category_id(self) -> Optional[UUID]:
        return self.category_id
    
    rbacobject = resolve_rbacobject
    
    @strawberry.field(
        description="""Related events""",
        permission_classes=[OnlyForAuthentized(isList=True)])
    async def events(self, info: strawberry.types.Info) -> List[EventGQLModel]:
        loader = getLoadersFromInfo(info).events
        result = await loader.filter_by(eventtype_id=self.id)
        return result

    @strawberry.field(
        description="Category of event type",
        permission_classes=[OnlyForAuthentized()])
    async def category(self, info: strawberry.types.Info) -> Optional["EventCategoryGQLModel"]:
        from .EventCategoryGQLModel import EventCategoryGQLModel
        result = await EventCategoryGQLModel.resolve_reference(info=info, id=self.category_id)
        return result

EventWhereFilter = Annotated["EventWhereFilter", strawberry.lazy(".EventGQLModel")]

@createInputs
@dataclass
class EventTypeWhereFilter:
    id: UUID
    name: str
    name_en: str

    valid: bool
    created: datetime.datetime
    createdby: UUID
    changedby: UUID

    category_id: UUID

    from .EventCategoryGQLModel import EventCategoryWhereFilter
    category: EventCategoryWhereFilter
    
    events: EventWhereFilter



#Queries
@strawberry.field(
    description="Finds a particular event type",
        permission_classes=[OnlyForAuthentized()])
async def event_type_by_id(self, info: strawberry.types.Info, id: UUID) -> Optional[EventTypeGQLModel]:
    result = await EventTypeGQLModel.resolve_reference(info=info, id=id)
    return result

@strawberry.field(
    description="""Finds all event types paged""",
        permission_classes=[OnlyForAuthentized(isList=True)])
@asPage
async def event_type_page(self, info: strawberry.types.Info, skip: int = 0, limit: int = 10, where: Optional[EventTypeWhereFilter] = None) -> List[EventTypeGQLModel]:
    return getLoadersFromInfo(info).eventtypes


#Mutations
@strawberry.input(description="Input structure - C operation")
class EventTypeInsertGQLModel:
    name: str = strawberry.field(description="name of event type")
    category_id: UUID = strawberry.field(description="category of event type")

    id: Optional[UUID] = strawberry.field(description="primary key (UUID), could be client generated", default=None)
    name_en: Optional[str] = strawberry.field(description="name of event type in English", default="")
    
    valid: Optional[bool] = True
    createdby: strawberry.Private[UUID] = None


@strawberry.input(description="Input structure - UD operation")
class EventTypeUpdateGQLModel:
    id: UUID = strawberry.field(description="primary key (UUID), identifies object of operation")
    lastchange: datetime.datetime = strawberry.field(description="timestamp of last change = TOKEN")

    name: Optional[str] = strawberry.field(description="name of event type", default=None)
    name_en: Optional[str] = strawberry.field(description="name of event type in English", default=None)

    valid: Optional[bool] = None
    changedby: strawberry.Private[UUID] = None

    category_id: Optional[UUID] = strawberry.field(description="category of event type", default=None)


@strawberry.type(description="Result of CUD operation")
class EventTypeResultGQLModel:
    id: UUID = strawberry.field(description="primary key of CUD operation object")
    msg: str = strawberry.field(description=\
        """Should be `ok` if descired state has been reached, otherwise `fail`. For update operation fail should be also stated when bad lastchange has been entered.""")

    @strawberry.field(description="""Result of event type operation""")
    async def type(self, info: strawberry.types.Info) -> Optional[EventTypeGQLModel]:
        result = await EventTypeGQLModel.resolve_reference(info=info, id=self.id)
        return result
    
@strawberry.mutation(
    description="C operation",
        permission_classes=[OnlyForAuthentized()])
async def event_type_insert(self, info: strawberry.types.Info, event_type: EventTypeInsertGQLModel) -> EventTypeResultGQLModel:
    user = getUserFromInfo(info)
    event_type.createdby = UUID(user["id"])

    loader = getLoadersFromInfo(info).eventtypes
    row = await loader.insert(event_type)
    result = EventTypeResultGQLModel(id=row.id, msg="ok")
    return result


@strawberry.mutation(
    description="U operation",
        permission_classes=[OnlyForAuthentized()])
async def event_type_update(self, info: strawberry.types.Info, event_type: EventTypeUpdateGQLModel) -> EventTypeResultGQLModel:
    user = getUserFromInfo(info)
    event_type.changedby = UUID(user["id"])

    loader = getLoadersFromInfo(info).eventtypes
    row = await loader.update(event_type)
    result = EventTypeResultGQLModel(id=event_type.id, msg="ok")
    result.msg = "fail" if row is None else "ok"
    return result