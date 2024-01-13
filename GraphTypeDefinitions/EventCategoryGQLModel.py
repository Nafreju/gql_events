import strawberry
import datetime
from typing import List, Annotated, Optional
from ._GraphResolvers import asPage, asForeignList, createRootResolver_by_id
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
    
    @strawberry.field(description="""Validity of event category""",
        permission_classes=[OnlyForAuthentized()])
    def valid(self) -> Optional[bool]:
        return self.valid
    
    created = resolve_created
    lastchange = resolve_lastchange
    createdby = resolve_createdby
    changedby = resolve_changedby
    rbacobject = resolve_rbacobject


    @strawberry.field(
        description="""event types which has this category""",
        permission_classes=[OnlyForAuthentized(isList=True)])
    @asForeignList(foreignKeyName="category_id")
    async def event_types(self, info: strawberry.types.Info) -> List[EventTypeGQLModel]:
        return getLoadersFromInfo(info).eventtypes



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

    event_types: EventTypeWhereFilter




#Queries


event_category_by_id = createRootResolver_by_id(EventCategoryGQLModel, description="""Finds a particular event category""")


@strawberry.field(
    description="""Finds all event categories paged""",
        permission_classes=[OnlyForAuthentized(isList=True)])
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
    description="C operation",
        permission_classes=[OnlyForAuthentized()])
async def event_category_insert(self, info: strawberry.types.Info, event_category: EventCategoryInsertGQLModel) -> EventCategoryResultGQLModel:
    user = getUserFromInfo(info)
    event_category.createdby = UUID(user["id"])

    loader = getLoadersFromInfo(info).eventcategories
    row = await loader.insert(event_category)
    result = EventCategoryResultGQLModel(id=row.id, msg="ok")
    return result

@strawberry.mutation(
    description="U operation",
        permission_classes=[OnlyForAuthentized()])
async def event_category_update(self, info: strawberry.types.Info, event_category: EventCategoryUpdateGQLModel) -> EventCategoryResultGQLModel: 
    user = getUserFromInfo(info)
    event_category.changedby = UUID(user["id"])
        
    loader = getLoadersFromInfo(info).eventcategories
    row = await loader.update(event_category)
    result = EventCategoryResultGQLModel(id=event_category.id, msg="ok")
    result.msg = "fail" if row is None else "ok"
    return result