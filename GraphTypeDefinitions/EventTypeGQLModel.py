import strawberry
import datetime
from typing import Union, List, Annotated, Optional
from ._GraphResolvers import asPage
from uuid import UUID
from dataclasses import dataclass
from uoishelpers.resolvers import createInputs
from utils import getLoadersFromInfo, getUserFromInfo

EventGQLModel = Annotated["EventGQLModel", strawberry.lazy(".EventGQLModel")]
EventCategoryGQLModel = Annotated["EventCategoryGQLModel", strawberry.lazy(".EventCategoryGQLModel")]


@strawberry.federation.type(keys=["id"], description="""Represents an event type""")
class EventTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: UUID):
        loader = getLoadersFromInfo(info).eventtypes
        result = await loader.load(id)
        if result is not None:
            result.__strawberry_definition__ = cls.__strawberry_definition__  # little hack :)
        return result
    
    @strawberry.field(description="""Primary key""")
    def id(self) -> UUID:
        return self.id

    @strawberry.field(description="""Name of event type""")
    def name(self) -> Optional[str]:
        return self.name

    @strawberry.field(description="""Name of event type in English""")
    def name_en(self) -> Optional[str]:
        return self.name_en
    
    @strawberry.field(description="""Validity of event type""")
    def valid(self) -> Optional[bool]:
        return self.valid
    
    @strawberry.field(description="""When event type was created""")
    def created(self) -> Optional[datetime.datetime]:
        return self.created

    @strawberry.field(description="""Time stamp""")
    def lastchange(self) -> Optional[datetime.datetime]:
        return self.lastchange

    @strawberry.field(description="""By whom event type was created""")
    def createdby(self) -> Optional[UUID]:
        return self.createdby

    @strawberry.field(description="""Who changed the event type""")
    def changedby(self) -> Optional[UUID]:
        return self.changedby

    @strawberry.field(description="""Category id of event type""")
    def category_id(self) -> Optional[UUID]:
        return self.category_id
    
    #TODO resolve RBACObject
    


    @strawberry.field(description="""Related events""")
    async def events(self, info: strawberry.types.Info) -> Optional[List[EventGQLModel]]:
        loader = getLoadersFromInfo(info).events
        result = await loader.filter_by(eventtype_id=self.id)
        return result


    @strawberry.field(description="Category of event type")
    async def category(self, info: strawberry.types.Info) -> Optional["EventCategoryGQLModel"]:
        from .EventCategoryGQLModel import EventCategoryGQLModel
        result = await EventCategoryGQLModel.resolve_reference(info=info, id=self.category_id)
        return result


@createInputs
@dataclass
class EventTypeWhereFilter:
    id: UUID
    name: str
    name_en: str

    from .EventCategoryGQLModel import EventCategoryWhereFilter
    category: EventCategoryWhereFilter

#Queries
@strawberry.field(description="Finds a particular event type")
async def event_type_by_id(self, info: strawberry.types.Info, id: UUID) -> Optional[EventTypeGQLModel]:
    result = await EventTypeGQLModel.resolve_reference(info=info, id=id)
    return result

@strawberry.field(description="""Finds all event types paged""")
@asPage
async def event_type_page(self, info: strawberry.types.Info, skip: int = 0, limit: int = 10, where: Optional[EventTypeWhereFilter] = None) -> List[EventTypeGQLModel]:
    return getLoadersFromInfo(info).eventtypes


#Mutations
@strawberry.input(description="Input structure - C operation")
class EventTypeInsertGQLModel:
    name: str = strawberry.field(description="name of event type")

    id: Optional[UUID] = strawberry.field(description="primary key (UUID), could be client generated", default=None)
    name_en: Optional[str] = strawberry.field(description="name of event type in English", default="")
    category_id: Optional[UUID] = strawberry.field(description="category of event type", default=None)
    
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
    
@strawberry.mutation(description="C operation")
async def event_type_insert(self, info: strawberry.types.Info, event_type: EventTypeInsertGQLModel) -> EventTypeResultGQLModel:
    user = getUserFromInfo(info) #TODO
    #event.changedby = UUID(user["id"])

    loader = getLoadersFromInfo(info).eventtypes
    row = await loader.insert(event_type)
    result = EventTypeResultGQLModel(id=row.id, msg="ok")
    return result


@strawberry.mutation(description="U operation")
async def event_type_update(self, info: strawberry.types.Info, event_type: EventTypeUpdateGQLModel) -> EventTypeResultGQLModel:
    user = getUserFromInfo(info) #TODO
    #event.changedby = UUID(user["id"])

    loader = getLoadersFromInfo(info).eventtypes
    row = await loader.update(event_type)
    result = EventTypeResultGQLModel(id=event_type.id, msg="ok")
    result.msg = "fail" if row is None else "ok"
    return result