import strawberry
import datetime
from typing import Union, List, Annotated, Optional
from .utils import withInfo, getLoaders, getUser, asPage

from uuid import UUID
from dataclasses import dataclass
from uoishelpers.resolvers import createInputs


GroupGQLModel = Annotated["GroupGQLModel", strawberry.lazy(".externals")]
EventGQLModel = Annotated["EventGQLModel", strawberry.lazy(".EventGQLModel")]



@strawberry.federation.type(keys=["id"], description="""Describes a relation of an group to the event.""")
class EventGroupGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: UUID):
        loader = getLoaders(info).eventgroups
        result = await loader.load(id)
        if result is not None:
            result.__strawberry_definition__ = cls.__strawberry_definition__  # little hack :)
        return result
    
    @strawberry.field(description="""Primary key""")
    def id(self) -> UUID:
        return self.id
    
    @strawberry.field(description="""Event id""")
    def event_id(self) -> UUID:
        return self.event_id
    
    @strawberry.field(description="""Group id""")
    def group_id(self) -> UUID:
        return self.group_id

    
    @strawberry.field(description="""When this entity was created""")
    def created(self) -> Optional[datetime.datetime]:
        return self.created

    @strawberry.field(description="""Time stamp""")
    def lastchange(self) -> Optional[datetime.datetime]:
        return self.lastchange
    
    @strawberry.field(description="""By whom this entity was created""")
    def createdby(self) -> Optional[UUID]:
        return self.createdby

    @strawberry.field(description="""Who changed the this entity""")
    def changedby(self) -> Optional[UUID]:
        return self.changedby

    @strawberry.field(description="""Event assigned to group""")
    async def event(self, info: strawberry.types.Info) -> Optional[EventGQLModel]:
        from .EventGQLModel import EventGQLModel
        result = await EventGQLModel.resolve_reference(id=self.event_id)
        return result
@createInputs
@dataclass
class EventGroupWhereFilter:
    id:UUID
    event_id:int 
    group_id:int

#Queries
@strawberry.field(description="""Finds a particular event-group entity""")
async def event_group_by_id(self, info: strawberry.types.Info, id: UUID) -> Optional[EventGroupGQLModel]:
    result = await EventGroupGQLModel.resolve_reference(info=info, id=id)
    return getLoaders(info).eventgroup

@strawberry.field(description="""Finds all events-groups paged""")
@asPage
async def event_group_page(self, info: strawberry.types.Info, skip: int = 0, limit: int = 10, where: Optional[EventGroupWhereFilter] = None ) -> Optional[List[EventGroupGQLModel]]:

    return getLoaders(info).eventgroups

#Mutations
@strawberry.input(description="Input structure - C operation")
class EventGroupInsertGQLModel:
    event_id: UUID = strawberry.field(description="ID of event to be assigned to group")
    group_id: UUID = strawberry.field(description="ID of group to be assigned to event")

    id: Optional[UUID] = strawberry.field(description="primary key (UUID), could be client generated", default=None)
    createdby: strawberry.Private[UUID] = None

@strawberry.type(description="Result of CUD operations")
class EventGroupResultGQLModel:
    id: UUID = strawberry.field(description="primary key of CUD operation object")
    msg: str = strawberry.field(description=\
        """Should be `ok` if descired state has been reached, otherwise `fail`. For update operation fail should be also stated when bad lastchange has been entered.""")

    @strawberry.field(description="""Result of event-group operation""")
    async def event_group(self, info: strawberry.types.Info) -> Optional[EventGroupGQLModel]:
        result = await EventGroupGQLModel.resolve_reference(info=info, id=self.id)
        return result
    
@strawberry.mutation(description="C operation")
async def event_group_insert(self, info: strawberry.types.Info, event_group: EventGroupInsertGQLModel) -> EventGroupResultGQLModel:
    user = getUser(info) #TODO
    #event.changedby = UUID(user["id"])

    loader = getLoaders(info).eventgroups
    row = await loader.insert(event_group)
    result = EventGroupResultGQLModel(id=row.id, msg="ok")
    return result

