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

UserGQLModel = Annotated["UserGQLModel", strawberry.lazy(".externals")]
PresenceTypeGQLModel = Annotated["PresenceTypeGQLModel", strawberry.lazy(".PresenceTypeGQLModel")]
InvitationTypeGQLModel = Annotated["InvitationTypeGQLModel", strawberry.lazy(".InvitationTypeGQLModel")]
EventGQLModel = Annotated["EventGQLModel", strawberry.lazy(".EventGQLModel")]

@strawberry.federation.type(
    keys=["id"], description="""Describes a relation of an user to the event by invitation (like invited) and participation (like absent)""")
class PresenceGQLModel(BaseGQLModel):

    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).presences

    id = resolve_id
    
    @strawberry.field(description="""ID of event which is presence related to""",
        permission_classes=[OnlyForAuthentized()])
    def event_id(self) -> Optional[UUID]:
        return self.event_id
    
    @strawberry.field(description="""ID of user which is presence related to""",
        permission_classes=[OnlyForAuthentized()])
    def user_id(self) -> Optional[UUID]:
        return self.user_id
    
    @strawberry.field(description="""ID of invitation which is presence related to""",
        permission_classes=[OnlyForAuthentized()])
    def invitationtype_id(self) -> Optional[UUID]:
        return self.invitationtype_id
    
    @strawberry.field(description="""ID of presence type which is presence related to""",
        permission_classes=[OnlyForAuthentized()])
    def presencetype_id(self) -> Optional[UUID]:
        return self.presencetype_id

    created = resolve_created
    lastchange = resolve_lastchange
    createdby = resolve_createdby
    changedby = resolve_changedby
    
    rbacobject = resolve_rbacobject


    @strawberry.field(description="""The event""",
        permission_classes=[OnlyForAuthentized()])
    async def event(self, info: strawberry.types.Info) -> Optional[EventGQLModel]:
        from .EventGQLModel import EventGQLModel
        result = await EventGQLModel.resolve_reference(info, id=self.event_id)
        return result

    @strawberry.field(description="""Present, Vacation etc.""",
        permission_classes=[OnlyForAuthentized()])
    async def presence_type(self, info: strawberry.types.Info) -> Optional[PresenceTypeGQLModel]:
        from .PresenceTypeGQLModel import PresenceTypeGQLModel
        result = await PresenceTypeGQLModel.resolve_reference(info, self.presencetype_id)
        return result

    @strawberry.field(description="""Invited, Accepted, etc.""",
        permission_classes=[OnlyForAuthentized()])
    async def invitation_type(self, info: strawberry.types.Info) -> Optional[InvitationTypeGQLModel]:
        from .InvitationTypeGQLModel import InvitationTypeGQLModel
        result = await InvitationTypeGQLModel.resolve_reference(info, self.invitationtype_id)
        return result

    @strawberry.field(description="""The user / participant""",
        permission_classes=[OnlyForAuthentized()])
    def user(self) -> Optional["UserGQLModel"]:
        from .externals import UserGQLModel
        result = UserGQLModel(id=self.user_id)
        return result

@createInputs
@dataclass
class PresenceWhereFilter:
    id: UUID
    event_id: UUID
    user_id: UUID
    invitationtype_id: UUID
    presencetype_id: UUID

    created:bool
    createdby: UUID
    changedby: UUID

    from .EventGQLModel import EventWhereFilter
    event: EventWhereFilter

    from .PresenceTypeGQLModel import PresenceTypeWhereFilter
    presencetype: PresenceTypeWhereFilter

    from .InvitationTypeGQLModel import InvitationTypeWhereFilter
    invitationtype: InvitationTypeWhereFilter
    #TODO user

#Queries
@strawberry.field(
    description="""Finds a particular presence""",
        permission_classes=[OnlyForAuthentized()])
async def presence_by_id(self, info: strawberry.types.Info, id: UUID) -> Optional[PresenceGQLModel]:
    result = await PresenceGQLModel.resolve_reference(info, id=id)
    return result

@strawberry.field(
    description="""Finds all presences paged""",
        permission_classes=[OnlyForAuthentized(isList=True)])
@asPage
async def presence_page(self, info: strawberry.types.Info, skip: int = 0, limit: int = 10, where: Optional[PresenceWhereFilter] = None) -> List[PresenceGQLModel]:
    return getLoadersFromInfo(info).presences
    

#Mutations
@strawberry.input(description="Input structure - C operation")
class PresenceInsertGQLModel:
    user_id: UUID = strawberry.field(description="ID of user who is related to event")
    event_id: UUID = strawberry.field(description="ID of event which is related to user")
    invitationtype_id: UUID = strawberry.field(description="ID of invitation type related to event/user")#default value?
    presencetype_id: UUID = strawberry.field(description="type of presence related to event/user")#default?
    
    id: Optional[UUID] = strawberry.field(description="primary key (UUID), could be client generated", default=None)

    #valid: Optional[bool] = True
    createdby: strawberry.Private[UUID] = None


@strawberry.input(description="Input structure - UD operation")
class PresenceUpdateGQLModel:
    id: UUID = strawberry.field(description="primary key (UUID), identifies object of operation")
    lastchange: datetime.datetime = strawberry.field(description="timestamp of last change = TOKEN")

    #event_id: Optional[UUID] = strawberry.field(description="event which is assigned to user", default=None)
    #user_id: Optional[UUID] = strawberry.field(description="user which is assigned to event", default=None)
    
    invitationtype_id: Optional[UUID] = strawberry.field(description="invitation type which is assigned to presence", default=None)
    presencetype_id: Optional[UUID] = strawberry.field(description="presence type which is assigned to presence", default=None)

    #valid: Optional[bool] = None
    changedby: strawberry.Private[UUID] = None

    
@strawberry.type(description="Result of CUD operations")
class PresenceResultGQLModel:
    id: UUID = strawberry.field(description="primary key of CUD operation object")
    msg: str = strawberry.field(description=\
        """Should be `ok` if descired state has been reached, otherwise `fail`. For update operation fail should be also stated when bad lastchange has been entered.""")

    @strawberry.field(description="""Result of presence operation""")
    async def presence(self, info: strawberry.types.Info) -> Optional[PresenceGQLModel]:
        result = await PresenceGQLModel.resolve_reference(info=info, id=self.id)
        return result
    
@strawberry.mutation(
    description="C operation",
        permission_classes=[OnlyForAuthentized()])
async def presence_insert(self, info: strawberry.types.Info, presence: PresenceInsertGQLModel) -> PresenceResultGQLModel:
    user = getUserFromInfo(info)
    presence.createdby = UUID(user["id"])

    loader = getLoadersFromInfo(info).presences
    row = await loader.insert(presence)
    result = PresenceResultGQLModel(id=row.id, msg="ok")
    return result

@strawberry.mutation(
    description="U operation",
        permission_classes=[OnlyForAuthentized()])
async def presence_update(self, info: strawberry.types.Info, presence: PresenceUpdateGQLModel) -> PresenceResultGQLModel:
    user = getUserFromInfo(info)
    presence.changedby = UUID(user["id"])

    loader = getLoadersFromInfo(info).presences
    row = await loader.update(presence)
    result = PresenceResultGQLModel(id=presence.id, msg="ok")
    result.msg = "fail" if row is None else "ok"
    return result


@strawberry.input(description="Input structure - D operation")
class PresenceDeleteGQLModel:
    id: UUID = strawberry.field(description="The ID of the project")
    lastchange: datetime.datetime = strawberry.field(description="timestamp of last change = TOKEN")

@strawberry.mutation(
    description="D operation",
        permission_classes=[OnlyForAuthentized()])
async def presence_delete(self, info: strawberry.types.Info, id: UUID) -> PresenceResultGQLModel:
    loader = getLoadersFromInfo(info).presences
    row = await loader.delete(id=id)
    result = PresenceResultGQLModel(id=id, msg="ok")
    result.msg = "fail" if row is None else "ok"
    return result
