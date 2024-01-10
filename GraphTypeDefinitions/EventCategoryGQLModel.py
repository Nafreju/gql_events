import strawberry
import datetime
from typing import Union, List, Annotated, Optional
from ._GraphResolvers import asPage
from utils import getLoadersFromInfo, getUserFromInfo
from uuid import UUID
from dataclasses import dataclass
from uoishelpers.resolvers import createInputs
from ._GraphPermissions import OnlyForAuthentized


EventTypeGQLModel = Annotated["EventTypeGQLModel", strawberry.lazy(".EventTypeGQLModel")]

@strawberry.federation.type(keys=["id"], description="""Represents category of event""")
class EventCategoryGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: UUID):
        loader = getLoadersFromInfo(info).eventcategories
        result = await loader.load(id)
        if result is not None:
            result.__strawberry_definition__ = cls.__strawberry_definition__   # little hack :)
        return result

    @strawberry.field(description="""Primary key""")
    def id(self) -> UUID:
        return self.id

    @strawberry.field(description="""Name of event category""")
    def name(self) -> str:
        return self.name

    @strawberry.field(description=""""Name of event category in English""")
    def name_en(self) -> str:
        return self.name_en

    @strawberry.field(description="""Validity of event category""")
    def valid(self) -> Optional[bool]:
        return self.valid
    
    @strawberry.field(description="""When event category was created""")
    def created(self) -> Optional[datetime.datetime]:
        return self.created

    @strawberry.field(description="""Time stamp""")
    def lastchange(self) -> Optional[datetime.datetime]:
        return self.lastchange
    
    @strawberry.field(description="""By whom event category was created""")
    def createdby(self) -> Optional[UUID]:
        return self.createdby

    @strawberry.field(description="""Who changed the event category""")
    def changedby(self) -> Optional[UUID]:
        return self.changedby
    
    RBACObjectGQLModel = Annotated["RBACObjectGQLModel", strawberry.lazy(".externals")]
    @strawberry.field(description="""Who made last change""")
    async def resolve_rbacobject(self, info: strawberry.types.Info) -> Optional[RBACObjectGQLModel]:
        from .externals import RBACObjectGQLModel
        result = None if self.rbacobject is None else await RBACObjectGQLModel.resolve_reference(info, self.rbacobject)
        return result


    @strawberry.field(description="""event types which has this category""")
    async def types(self, info: strawberry.types.Info) -> List[EventTypeGQLModel]:
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

    #types: EventTypeWhereFilter




#Queries
@strawberry.field(description="""Finds a particular event category""")
async def event_category_by_id(self, info: strawberry.types.Info, id: UUID) -> Optional[EventCategoryGQLModel]:
    result = await EventCategoryGQLModel.resolve_reference(info=info, id=id)
    return result

@strawberry.field(description="""Finds all event categories paged""")
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
    msg: str = strawberry.field(description=\
        """Should be `ok` if descired state has been reached, otherwise `fail`. For update operation fail should be also stated when bad lastchange has been entered.""")

    @strawberry.field(description="""Result of event category operation""")
    async def category(self, info: strawberry.types.Info) -> Optional[EventCategoryGQLModel]:
        result = await EventCategoryGQLModel.resolve_reference(info=info, id=self.id)
        return result
    
@strawberry.mutation(description="C operation")
async def event_category_insert(self, info: strawberry.types.Info, event_category: EventCategoryInsertGQLModel) -> EventCategoryResultGQLModel:
    user = getUserFromInfo(info) #TODO
    #event.changedby = UUID(user["id"])

    loader = getLoadersFromInfo(info).eventcategories
    row = await loader.insert(event_category)
    result = EventCategoryResultGQLModel(id=row.id, msg="ok")
    return result

@strawberry.mutation(description="U operation")
async def event_category_update(self, info: strawberry.types.Info, event_category: EventCategoryUpdateGQLModel) -> EventCategoryResultGQLModel: 
    user = getUserFromInfo(info) #TODO
    #event.changedby = UUID(user["id"])
        
    loader = getLoadersFromInfo(info).eventcategories
    row = await loader.update(event_category)
    result = EventCategoryResultGQLModel(id=event_category.id, msg="ok")
    result.msg = "fail" if row is None else "ok"
    return result