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
    asPage
)

GroupGQLModel = Annotated["GroupGQLModel", strawberry.lazy(".externals")]
EventGQLModel = Annotated["EventGQLModel", strawberry.lazy(".EventGQLModel")]



@strawberry.federation.type(
    keys=["id"], description="""Describes a relation of an group to the event.""")
class EventGroupGQLModel(BaseGQLModel):

    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).eventgroups

    id = resolve_id
    name = resolve_name
    changedby = resolve_changedby
    lastchange = resolve_lastchange
    created = resolve_created
    createdby = resolve_createdby
    name_en = resolve_name_en
    rbacobject = resolve_rbacobject


    @strawberry.field(
        description="""Event assigned to group""")
    async def event(self, info: strawberry.types.Info) -> Optional[EventGQLModel]:
        from .EventGQLModel import EventGQLModel
        result = await EventGQLModel.resolve_reference(info=info, id=self.event_id)
        return result
    
    @strawberry.field(
        description="""Group assigned to event""")
    async def group(self, info: strawberry.types.Info) -> Optional[GroupGQLModel]:
        from .externals import GroupGQLModel
        result = await GroupGQLModel.resolve_reference(info=info, id=self.group_id)
        return result
    
@createInputs
@dataclass
class EventGroupWhereFilter:
    id: UUID
    event_id: UUID 
    group_id: UUID

    created: datetime.datetime
    createdby: UUID
    changedby: UUID

    #TODO event

#Queries
@strawberry.field(
    description="""Finds a particular event-group entity""")
async def event_group_by_id(self, info: strawberry.types.Info, id: UUID) -> Optional[EventGroupGQLModel]:
    result = await EventGroupGQLModel.resolve_reference(info=info, id=id)
    return result


@strawberry.field(description="""Finds all events-groups paged""")
@asPage
async def event_group_page(self, info: strawberry.types.Info, skip: int = 0, limit: int = 10, where: Optional[EventGroupWhereFilter] = None ) -> List[EventGroupGQLModel]:
    return getLoadersFromInfo(info).eventgroups

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
    
@strawberry.mutation(
    description="C operation")
async def event_group_insert(self, info: strawberry.types.Info, event_group: EventGroupInsertGQLModel) -> EventGroupResultGQLModel:
    user = getUserFromInfo(info) #TODO
    #event.changedby = UUID(user["id"])

    loader = getLoadersFromInfo(info).eventgroups
    row = await loader.insert(event_group)
    result = EventGroupResultGQLModel(id=row.id, msg="ok")
    return result


#TODO delete
