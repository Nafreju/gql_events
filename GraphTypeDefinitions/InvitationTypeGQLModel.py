import strawberry
import datetime
from typing import Union, List, Annotated, Optional
from ._GraphResolvers import asPage
from uuid import UUID
from dataclasses import dataclass
from uoishelpers.resolvers import createInputs
from utils import getLoadersFromInfo, getUserFromInfo



@strawberry.federation.type(keys=["id"], description="""Represents type of invitation user obtained to event""")
class InvitationTypeGQLModel:

    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: UUID):
        loader = getLoadersFromInfo(info).invitationtypes
        result = await loader.load(id)
        if result is not None:
            result.__strawberry_definition__ = cls.__strawberry_definition__   # little hack :)
        return result

    @strawberry.field(description="""Primary key""")
    def id(self) -> UUID:
        return self.id

    @strawberry.field(description="""Name of invitation type""")
    def name(self) -> str:
        return self.name

    @strawberry.field(description="""Name of invitation type in English""")
    def name_en(self) -> str:
        return self.name_en

    @strawberry.field(description="""Validity of invitation type""")
    def valid(self) -> Optional[bool]:
        return self.valid
    
    @strawberry.field(description="""When invitation type was created""")
    def created(self) -> Optional[datetime.datetime]:
        return self.created

    @strawberry.field(description="""Time stamp""")
    def lastchange(self) -> Optional[datetime.datetime]:
        return self.lastchange
    
    @strawberry.field(description="""By whom invitation type was created""")
    def createdby(self) -> Optional[UUID]:
        return self.createdby

    @strawberry.field(description="""Who changed the invitation type""")
    def changedby(self) -> Optional[UUID]:
        return self.changedby
    
    RBACObjectGQLModel = Annotated["RBACObjectGQLModel", strawberry.lazy(".externals")]
    @strawberry.field(description="""Who made last change""")
    async def resolve_rbacobject(self, info: strawberry.types.Info) -> Optional[RBACObjectGQLModel]:
        from .externals import RBACObjectGQLModel
        result = None if self.rbacobject is None else await RBACObjectGQLModel.resolve_reference(info, self.rbacobject)
        return result  

    #TODO def presences - need PresenceGQLModel which works

@createInputs
@dataclass
class InvitationTypeWhereFilter:
    id: UUID
    name: str
    name_en: str

    valid: bool
    created: datetime.datetime
    createdby: UUID 
    changedby: UUID 



#Queries
@strawberry.field(
    description="""Finds a particular invitation type""")
async def invitation_type_by_id(self, info: strawberry.types.Info, id: UUID) -> Optional[InvitationTypeGQLModel]:
    result = await InvitationTypeGQLModel.resolve_reference(info=info, id=id)
    return result

@strawberry.field(
    description="""Finds all invitation types paged""")
@asPage
async def invitation_type_page(self, info: strawberry.types.Info, skip: int = 0, limit: int = 10, where: Optional[InvitationTypeWhereFilter] = None) -> List[InvitationTypeGQLModel]:
    return getLoadersFromInfo(info).invitationtypes



#Mutations
@strawberry.input(description="Input structure - C operation")
class InvitationTypeInsertGQLModel:
    name: str = strawberry.field(description="name of invitation type")

    id: Optional[UUID] = strawberry.field(description="primary key (UUID), could be client generated", default=None)
    name_en: Optional[str] = strawberry.field(description="name of invitation type in English", default="")

    valid: Optional[bool] = True
    createdby: strawberry.Private[UUID] = None


@strawberry.input(description="Input structure UD operation")
class InvitationTypeUpdateGQLModel:
    id: UUID = strawberry.field(description="primary key (UUID), identifies object of operation")
    lastchange: datetime.datetime = strawberry.field(description="timestamp of last change = TOKEN")

    name: Optional[str] = strawberry.field(description="name of invitation type", default=None)
    name_en: Optional[str] = strawberry.field(description="name of invitation type in English", default=None)

    valid: Optional[bool] = None
    changedby: strawberry.Private[UUID] = None


@strawberry.type(description="Result of CUD operations")
class InvitationTypeResultGQLModel:
    id: UUID = strawberry.field(description="primary key of CUD operation object")
    msg: str = strawberry.field(description=\
        """Should be `ok` if descired state has been reached, otherwise `fail`. For update operation fail should be also stated when bad lastchange has been entered.""")

    @strawberry.field(description="""Result of invitation type operation""")
    async def type(self, info: strawberry.types.Info) -> Optional[InvitationTypeGQLModel]:
        result = await InvitationTypeGQLModel.resolve_reference(info=info, id=self.id)
        return result


@strawberry.mutation(
    description="C operation")
async def invitation_type_insert(self, info: strawberry.types.Info, invitation_type: InvitationTypeInsertGQLModel) -> InvitationTypeResultGQLModel:
    user = getUserFromInfo(info) #TODO
    #event.changedby = UUID(user["id"])

    loader = getLoadersFromInfo(info).invitationtypes
    row = await loader.insert(invitation_type)
    result = InvitationTypeResultGQLModel(id=row.id, msg="ok")
    return result


@strawberry.mutation(
    description="U operation")
async def invitation_type_update(self, info: strawberry.types.Info, invitation_type: InvitationTypeUpdateGQLModel) -> InvitationTypeResultGQLModel: 
    user = getUserFromInfo(info) #TODO
    #event.changedby = UUID(user["id"])
        
    loader = getLoadersFromInfo(info).invitationtypes
    row = await loader.update(invitation_type)
    result = InvitationTypeResultGQLModel(id=invitation_type.id, msg="ok")
    result.msg = "fail" if row is None else "ok"
    return result