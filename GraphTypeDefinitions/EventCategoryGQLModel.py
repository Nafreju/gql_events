import strawberry
import datetime
from typing import List, Annotated, Optional
from ._GraphResolvers import asPage, resolve_result_msg
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
    createRootResolver_by_id,
    asPage
)


EventTypeGQLModel = Annotated["EventTypeGQLModel", strawberry.lazy(".EventTypeGQLModel")]

@strawberry.federation.type(
    keys=["id"], description="""Represents category of event""")
class EventCategoryGQLModel(BaseGQLModel):

    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).eventcategories

    # @classmethod
    # async def resolve_reference(cls, info: strawberry.types.Info, id: uuid.UUID):
    # implementation is inherited

    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en
    
    @strawberry.field(description="""Validity of event category""")
    def valid(self) -> Optional[bool]:
        return self.valid
    
    created = resolve_created
    lastchange = resolve_lastchange
    createdby = resolve_createdby
    changedby = resolve_changedby
    rbacobject = resolve_rbacobject


    @strawberry.field(
        description="""event types which has this category""")
    async def event_types(self, info: strawberry.types.Info) -> List[EventTypeGQLModel]:
        loader = getLoadersFromInfo(info).eventtypes
        result = await loader.filter_by(category_id=self.id)
        return result


EventTypeWhereFilter = Annotated["EventTypeWhereFilter", strawberry.lazy(".EventTypeGQLModel")]

@createInputs
@dataclass
class EventCategoryWhereFilter:
    id: UUID
    name: str
    name_en: str

    valid: bool
    created: datetime.datetime
    createdby: UUID
    changedby: UUID

    #TODO maybe createRootResolver.... _GraphResolvers
    #types: EventTypeWhereFilter




#Queries

@strawberry.field(
    description="""Finds a particular event category""")
async def event_category_by_id(self, info: strawberry.types.Info, id: UUID) -> Optional[EventCategoryGQLModel]:
    result = await EventCategoryGQLModel.resolve_reference(info=info, id=id)
    return result


@strawberry.field(
    description="""Finds all event categories paged""")
@asPage
async def event_category_page(self, info: strawberry.types.Info, \
            skip: int = 0, limit: int = 10, where: Optional[EventCategoryWhereFilter] = None) -> List[EventCategoryGQLModel]:
    return getLoadersFromInfo(info).eventcategories



#Mutations
@strawberry.input(description="Input structure - C operation")
class EventCategoryInsertGQLModel:
    name: str = strawberry.field(description="name of event category")

    id: Optional[UUID] = strawberry.field(description="primary key (UUID), could be client generated", default=None)
    name_en: Optional[str] = strawberry.field(description="name of event category in English", default="")

    valid: Optional[bool] = True
    createdby: strawberry.Private[UUID] = None

@strawberry.input(description="Input structure UD operation")
class EventCategoryUpdateGQLModel:
    id: UUID = strawberry.field(description="primary key (UUID), identifies object of operation")
    lastchange: datetime.datetime = strawberry.field(description="timestamp of last change = TOKEN")

    name: Optional[str] = strawberry.field(description="name of event category", default=None)
    name_en: Optional[str] = strawberry.field(description="name of event category in English", default=None)

    valid: Optional[bool] = None
    changedby: strawberry.Private[UUID] = None


@strawberry.type(description="Result of CUD operations")
class EventCategoryResultGQLModel:
    id: UUID = strawberry.field(description="primary key of CUD operation object")
    msg: str = strawberry.field(description="""Should be `ok` if descired state has been reached, otherwise `fail`.
For update operation fail should be also stated when bad lastchange has been entered.""")


    @strawberry.field(description="""Result of event category operation""")
    async def category(self, info: strawberry.types.Info) -> Optional[EventCategoryGQLModel]:
        result = await EventCategoryGQLModel.resolve_reference(info=info, id=self.id)
        return result
    
@strawberry.mutation(
    description="C operation")
async def event_category_insert(self, info: strawberry.types.Info, event_category: EventCategoryInsertGQLModel) -> EventCategoryResultGQLModel:
    user = getUserFromInfo(info) #TODO
    #event.changedby = UUID(user["id"])

    loader = getLoadersFromInfo(info).eventcategories
    row = await loader.insert(event_category)
    result = EventCategoryResultGQLModel(id=row.id, msg="ok")
    return result

@strawberry.mutation(
    description="U operation")
async def event_category_update(self, info: strawberry.types.Info, event_category: EventCategoryUpdateGQLModel) -> EventCategoryResultGQLModel: 
    user = getUserFromInfo(info) #TODO
    #event.changedby = UUID(user["id"])
        
    loader = getLoadersFromInfo(info).eventcategories
    row = await loader.update(event_category)
    result = EventCategoryResultGQLModel(id=event_category.id, msg="ok")
    result.msg = "fail" if row is None else "ok"
    return result