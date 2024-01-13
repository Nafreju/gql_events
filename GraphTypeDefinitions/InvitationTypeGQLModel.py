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

PresenceGQLModel = Annotated["PresenceGQLModel", strawberry.lazy(".PresenceGQLModel")]


@strawberry.federation.type(
    keys=["id"], description="""Represents type of invitation user obtained to event""")
class InvitationTypeGQLModel(BaseGQLModel):

    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).invitationtypes

    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en

    @strawberry.field(description="""Validity of invitation type""",
        permission_classes=[OnlyForAuthentized()])
    def valid(self) -> Optional[bool]:
        return self.valid
    
    created = resolve_created
    lastchange = resolve_lastchange
    createdby = resolve_createdby
    changedby = resolve_changedby
    
    rbacobject = resolve_rbacobject
    
    @strawberry.field(
        description="""presences having this invitation""",
        permission_classes=[OnlyForAuthentized(isList=True)])
    async def presences(self, info: strawberry.types.Info) -> List[PresenceGQLModel]:
        loader = getLoadersFromInfo(info).presences
        result = await loader.filter_by(invitationtype_id=self.id)
        return result


PresenceWhereFilter = Annotated["PresenceWhereFilter", strawberry.lazy(".PresenceGQLModel")]

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

    presences: PresenceWhereFilter



#Queries
@strawberry.field(
    description="""Finds a particular invitation type""",
        permission_classes=[OnlyForAuthentized()])
async def invitation_type_by_id(self, info: strawberry.types.Info, id: UUID) -> Optional[InvitationTypeGQLModel]:
    result = await InvitationTypeGQLModel.resolve_reference(info=info, id=id)
    return result

@strawberry.field(
    description="""Finds all invitation types paged""",
        permission_classes=[OnlyForAuthentized(isList=True)])
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
    description="C operation",
        permission_classes=[OnlyForAuthentized()])
async def invitation_type_insert(self, info: strawberry.types.Info, invitation_type: InvitationTypeInsertGQLModel) -> InvitationTypeResultGQLModel:
    user = getUserFromInfo(info)
    invitation_type.createdby = UUID(user["id"])

    loader = getLoadersFromInfo(info).invitationtypes
    row = await loader.insert(invitation_type)
    result = InvitationTypeResultGQLModel(id=row.id, msg="ok")
    return result


@strawberry.mutation(
    description="U operation",
        permission_classes=[OnlyForAuthentized()])
async def invitation_type_update(self, info: strawberry.types.Info, invitation_type: InvitationTypeUpdateGQLModel) -> InvitationTypeResultGQLModel: 
    user = getUserFromInfo(info)
    invitation_type.changedby = UUID(user["id"])
        
    loader = getLoadersFromInfo(info).invitationtypes
    row = await loader.update(invitation_type)
    result = InvitationTypeResultGQLModel(id=invitation_type.id, msg="ok")
    result.msg = "fail" if row is None else "ok"
    return result