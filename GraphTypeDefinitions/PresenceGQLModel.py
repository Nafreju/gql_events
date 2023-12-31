import strawberry
import datetime
from typing import Union, List, Annotated, Optional
from .utils import getLoaders, getUser
from uuid import UUID

UserGQLModel = Annotated["UserGQLModel", strawberry.lazy(".externals")]
PresenceTypeGQLModel = Annotated["PresenceTypeGQLModel", strawberry.lazy(".PresenceTypeGQLModel")]
InvitationTypeGQLModel = Annotated["InvitationTypeGQLModel", strawberry.lazy(".InvitationTypeGQLModel")]
EventGQLModel = Annotated["EventGQLModel", strawberry.lazy(".EventGQLModel")]

@strawberry.federation.type(keys=["id"], description="""Describes a relation of an user to the event by invitation (like invited) and participation (like absent)""")
class PresenceGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: UUID):
        loader = getLoaders(info).presences
        result = await loader.load(id)
        if result is not None:
            result.__strawberry_definition__ = cls.__strawberry_definition__  # little hack :)
        return result

    @strawberry.field(description="""Primary key""")
    def id(self) -> UUID:
        return self.id
    
    @strawberry.field(description="""ID of event which is presence related to""")
    def event_id(self) -> Optional[UUID]:
        return self.event_id
    
    @strawberry.field(description="""ID of user which is presence related to""")
    def user_id(self) -> Optional[UUID]:
        return self.user_id
    
    @strawberry.field(description="""ID of invitation which is presence related to""")
    def invitationtype_id(self) -> Optional[UUID]:
        return self.invitationtype_id
    
    @strawberry.field(description="""ID of presence type which is presence related to""")
    def presencetype_id(self) -> Optional[UUID]:
        return self.presencetype_id

    # @strawberry.field(description="""Validity of presence""")
    # def valid(self) -> Optional[bool]:
    #     return self.valid
    
    @strawberry.field(description="""When presence was created""")
    def created(self) -> Optional[datetime.datetime]:
        return self.created
    
    @strawberry.field(description="""By whom presence was created""")
    def createdby(self) -> Optional[UUID]:
        return self.createdby

    @strawberry.field(description="""Who changed the presence""")
    def changedby(self) -> Optional[UUID]:
        return self.changedby
    
    @strawberry.field(description="""Time stamp""")
    def lastchange(self) -> Union[datetime.datetime, None]:
        return self.lastchange

    #TODO resolve RBACObject

    @strawberry.field(description="""Present, Vacation etc.""")
    async def presence_type(self, info: strawberry.types.Info) -> Optional[PresenceTypeGQLModel]:
        from .PresenceGQLModel import PresenceGQLModel
        result = await PresenceTypeGQLModel.resolve_reference(info, self.presencetype_id)
        return result

    @strawberry.field(description="""Invited, Accepted, etc.""")
    async def invitation_type(self, info: strawberry.types.Info) -> Optional[InvitationTypeGQLModel]:
        from .InvitationTypeGQLModel import InvitationTypeGQLModel
        result = await InvitationTypeGQLModel.resolve_reference(info, self.invitationtype_id)
        return result

    @strawberry.field(description="""The user / participant""")
    def user(self) -> Optional["UserGQLModel"]:
        from .externals import UserGQLModel
        result = UserGQLModel(id=self.user_id)
        return result

    @strawberry.field(description="""The event""")
    async def event(self, info: strawberry.types.Info) -> Optional[EventGQLModel]:
        from .EventGQLModel import EventGQLModel
        result = await EventGQLModel.resolve_reference(info, id=self.event_id)
        return result
    
#Queries
@strawberry.field(description="""Finds a particular presence""")
async def presence_by_id(self, info: strawberry.types.Info, id: UUID) -> Optional[PresenceGQLModel]:
    result = await PresenceGQLModel.resolve_reference(info, id=id)
    return result

@strawberry.field(description="""Finds all presences paged""")
async def presence_page(self, info: strawberry.types.Info, skip: int = 0, limit: int = 10) -> Optional[List[PresenceGQLModel]]:
    loader = getLoaders(info).presences
    result = await loader.page(skip, limit)
    return result

@strawberry.field(description="""Finds all presences for the event""")
async def presences_by_event(self, info: strawberry.types.Info, event_id: UUID) -> List[PresenceGQLModel]:
    loader = getLoaders(info).presences
    result = await loader.filter_by(event_id=event_id)
    return result

@strawberry.field(description="""Finds all presences for the user in the period""")
async def presences_by_user(self, info: strawberry.types.Info, user_id: UUID,) -> List[PresenceGQLModel]:
    #assert startdate < enddate, "startdate must be sooner than enddate"
    loader = getLoaders(info).presences
    # stmt = loader.getSelectStatement()
    # model = loader.getModel()
    # filterstmt = or_(
    #     and_(model.startdate >= startdate, model.enddate <= startdate),
    #     and_(model.startdate >= enddate, model.enddate <= enddate))
    # TODO
    # result = loader.execute_select(stmt.filter(filterstmt))
    result = await loader.filter_by(user_id=user_id)
    return result

#Mutations
@strawberry.input(description="Input structure - C operation")
class PresenceInsertGQLModel:
    user_id: UUID = strawberry.field(description="ID of user who is related to event")
    event_id: UUID = strawberry.field(description="ID of event which is related to user")
    invitationtype_id: UUID = strawberry.field(description="ID of invitation type related to event/user")#default value
    presencetype_id: Optional[UUID] = strawberry.field(description="type of presence related to event/user")#default to n
    
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
    
@strawberry.mutation(description="C operation")
async def presence_insert(self, info: strawberry.types.Info, presence: PresenceInsertGQLModel) -> PresenceResultGQLModel:
    user = getUser(info) #TODO
    #event.changedby = UUID(user["id"])

    loader = getLoaders(info).presences
    row = await loader.insert(presence)
    result = PresenceResultGQLModel(id=row.id, msg="ok")
    return result

@strawberry.mutation(description="U operation")
async def presence_update(self, info: strawberry.types.Info, presence: PresenceUpdateGQLModel) -> PresenceResultGQLModel:
    user = getUser(info) #TODO
    #event.changedby = UUID(user["id"])

    loader = getLoaders(info).presences
    row = await loader.update(presence)
    result = PresenceResultGQLModel(id=presence.id, msg="ok")
    result.msg = "fail" if row is None else "ok"
    return result