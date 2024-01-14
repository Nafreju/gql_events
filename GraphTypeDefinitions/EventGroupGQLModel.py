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

    resolve_changedby,
    resolve_created,
    resolve_lastchange,
    resolve_createdby,
    resolve_rbacobject,
    asPage
)
from ._GraphPermissions import OnlyForAuthentized

GroupGQLModel = Annotated["GroupGQLModel", strawberry.lazy(".externals")]
EventGQLModel = Annotated["EventGQLModel", strawberry.lazy(".EventGQLModel")]



@strawberry.federation.type(
    keys=["id"], description="""Describes a relation of an group to the event.""")
class EventGroupGQLModel(BaseGQLModel):

    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).eventgroups

    id = resolve_id

    @strawberry.field(description="""Event id""",
        permission_classes=[OnlyForAuthentized()])
    def event_id(self) -> UUID:
        return self.event_id
    
    @strawberry.field(description="""Group id""",
        permission_classes=[OnlyForAuthentized()])
    def group_id(self) -> UUID:
        return self.group_id

    created = resolve_created
    lastchange = resolve_lastchange
    changedby = resolve_changedby
    createdby = resolve_createdby
    rbacobject = resolve_rbacobject


    @strawberry.field(
        description="""Event assigned to group""",
        permission_classes=[OnlyForAuthentized()])
    async def event(self, info: strawberry.types.Info) -> Optional[EventGQLModel]:
        from .EventGQLModel import EventGQLModel
        result = await EventGQLModel.resolve_reference(info=info, id=self.event_id)
        return result
    
    @strawberry.field(
        description="""Group assigned to event""",
        permission_classes=[OnlyForAuthentized()])
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

    from .EventGQLModel import EventWhereFilter
    event: EventWhereFilter
    #TODO group

#Queries
@strawberry.field(
    description="""Finds a particular event-group entity""",
        permission_classes=[OnlyForAuthentized()])
async def event_group_by_id(self, info: strawberry.types.Info, id: UUID) -> Optional[EventGroupGQLModel]:
    result = await EventGroupGQLModel.resolve_reference(info=info, id=id)
    return result


@strawberry.field(description="""Finds all events-groups paged""",
        permission_classes=[OnlyForAuthentized(isList=True)])
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
    description="C operation",
        permission_classes=[OnlyForAuthentized()])
async def event_group_insert(self, info: strawberry.types.Info, event_group: EventGroupInsertGQLModel) -> EventGroupResultGQLModel:
    user = getUserFromInfo(info)
    event_group.createdby = UUID(user["id"])

    loader = getLoadersFromInfo(info).eventgroups
    row = await loader.insert(event_group)
    result = EventGroupResultGQLModel(id=row.id, msg="ok")
    return result



@strawberry.mutation(
    description="D operation",
        permission_classes=[OnlyForAuthentized()])
async def event_group_delete(self, info: strawberry.types.Info, event_group_id: UUID) -> EventGroupResultGQLModel:
    loader = getLoadersFromInfo(info).eventgroups
    row = await loader.delete(event_group_id)
    result = EventGroupResultGQLModel(id=event_group_id, msg="ok")
    result.msg = "fail" if row is None else "ok"
    return result