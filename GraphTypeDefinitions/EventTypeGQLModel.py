import strawberry
import datetime
from typing import Union, List, Annotated, Optional
from .utils import withInfo, getLoaders
from uuid import UUID

EventGQLModel = Annotated["EventGQLModel", strawberry.lazy(".EventGQLModel")]
CategoryGQLModel = Annotated["CategoryGQLModel", strawberry.lazy(".CategoryGQLModel")]


@strawberry.federation.type(keys=["id"], description="""Represents an event type""")
class EventTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: UUID):
        loader = getLoaders(info).eventtypes
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
    async def events(self, info: strawberry.types.Info) -> Optional[List["EventGQLModel"]]:
        loader = getLoaders(info).events
        result = await loader.filter_by(eventtype_id=self.id)
        return result

    
    """
    TODO
    @strawberry.field(description="Category of event type")
    async def category(self, info: strawberry.types.Info) -> Optional["CategoryGQLModel"]:
        result = await CategoryGQLModel.resolve_reference(info=info, id=self.category_id)
        return result
    """

#Queries
@strawberry.field(description="Finds a particular event type")
async def event_type_by_id(self, info: strawberry.types.Info, id: UUID) -> Optional[EventTypeGQLModel]:
    result = await EventTypeGQLModel.resolve_reference(info=info, id=id)
    return result

@strawberry.field(description="""Finds all event types paged""")
async def event_type_page(self, info: strawberry.types.Info, skip: int = 0, limit: int = 10) -> Optional[List[EventTypeGQLModel]]:
    loader = getLoaders(info).eventtypes
    result = await loader.page(skip, limit)
    return result


#Mutations
@strawberry.field(description="Input structure - C operation")
class EventTypeInsertGQLModel:
    name: str = strawberry.field(description="name of event type")

    id: Optional[UUID] = strawberry.field(description="primary key (UUID), could be client generated", default=None)
    name_en: Optional[str] = strawberry.field(description="name of event type in English", default=None)
    category_id: Optional[UUID] = strawberry.field(description="category of event type", default=None)
    
    valid: Optional[bool] = True
    createdby: strawberry.Private[UUID] = None


@strawberry.field(description="Input structure - UD operation")
class EventTypeUpdateGQLModel:
    id: UUID = strawberry.field(description="primary key (UUID), could be client generated")
    lastchange: datetime.datetime = strawberry.field(description="timestamp of last change = TOKEN")

    name: Optional[str] = strawberry.field(description="name of event type", default=None)
    name_en: Optional[str] = strawberry.field(description="name of event type in English", default=None)

    valid: Optional[bool] = strawberry.field(description="validity of event type")
    changedby: strawberry.Private[UUID] = None

    category_id: Optional[UUID] = strawberry.field(description="category of event type", default=None)


@strawberry.field(description="Result of CUD operation")
class EventTypeResultGQLModel:
    pass

