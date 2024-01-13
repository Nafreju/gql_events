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

PresenceGQLModel = Annotated["PresenceGQLModel", strawberry.lazy(".PresenceGQLModel")]


@strawberry.federation.type(
    keys=["id"], description="""Represents a type of presence (like Present)""")
class PresenceTypeGQLModel(BaseGQLModel):

    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).presencetypes

    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en

    @strawberry.field(description="""Validity of presence type""")
    def valid(self) -> Optional[bool]:
        return self.valid

    created = resolve_created
    lastchange = resolve_lastchange
    createdby = resolve_createdby
    changedby = resolve_changedby
    
    rbacobject = resolve_rbacobject

    @strawberry.field(
        description="Presences who have this presence type")
    async def presences(self, info: strawberry.types.Info) -> List[PresenceGQLModel]:
        loader = getLoadersFromInfo(info).presences
        result = await loader.filter_by(presencetype_id = self.id)
        return result
 
@createInputs
@dataclass
class PresenceTypeWhereFilter:
    id: UUID
    name: str
    name_en: str

    created: datetime.datetime
    valid: bool 
    createdby: UUID 
    changedby: UUID 

    #TODO presences



#Queries
@strawberry.field(
    description="""Finds a particular presence type""")
async def presence_type_by_id(self, info: strawberry.types.Info, id: UUID) -> Optional[PresenceTypeGQLModel]:
    result = await PresenceTypeGQLModel.resolve_reference(info=info, id=id)
    return result

@strawberry.field(
    description="""Finds all presence types paged""")
@asPage
async def presence_type_page(self, info: strawberry.types.Info, skip: int = 0, limit: int = 10, where: Optional[PresenceTypeWhereFilter] = None) -> List[PresenceTypeGQLModel]:
    return getLoadersFromInfo(info).presencetypes


#Mutations
@strawberry.input(description="Input structure - C operation")       
class PresenceTypeInsertGQLModel:
    name: str = strawberry.field(description="name of presence type")

    id: Optional[UUID] = strawberry.field(description="primary key (UUID), could be client generated", default=None)
    name_en: Optional[str] = strawberry.field(description="name of presence type in English", default="")
    
    valid: Optional[bool] = True
    createdby: strawberry.Private[UUID] = None


@strawberry.input(description="Input structure - UD operation")
class PresenceTypeUpdateGQLModel:
    id: UUID = strawberry.field(description="primary key (UUID), identifies object of operation")
    lastchange: datetime.datetime = strawberry.field(description="timestamp of last change = TOKEN")

    name: Optional[str] = strawberry.field(description="name of presence type", default=None)
    name_en: Optional[str] = strawberry.field(description="name of presence type in English", default=None)

    valid: Optional[bool] = None
    changedby: strawberry.Private[UUID] = None



@strawberry.type(description="Result of CUD operation")
class PresenceTypeResultGQLModel:
    id: UUID = strawberry.field(description="primary key of CUD operation object")
    msg: str = strawberry.field(description=\
        """Should be `ok` if descired state has been reached, otherwise `fail`. For update operation fail should be also stated when bad lastchange has been entered.""")

    @strawberry.field(description="""Result of presence type operation""")
    async def type(self, info: strawberry.types.Info) -> Optional[PresenceTypeGQLModel]:
        result = await PresenceTypeGQLModel.resolve_reference(info=info, id=self.id)
        return result
    

    
@strawberry.mutation(
    description="C operation")
async def presence_type_insert(self, info: strawberry.types.Info, presence_type: PresenceTypeInsertGQLModel) -> PresenceTypeResultGQLModel:
    user = getUserFromInfo(info) #TODO
    #event.changedby = UUID(user["id"])

    loader = getLoadersFromInfo(info).presencetypes
    row = await loader.insert(presence_type)
    result = PresenceTypeResultGQLModel(id=row.id, msg="ok")
    return result

@strawberry.mutation(
    description="U operation")
async def presence_type_update(self, info: strawberry.types.Info, presence_type: PresenceTypeUpdateGQLModel) -> PresenceTypeResultGQLModel:
    user = getUserFromInfo(info) #TODO
    #event.changedby = UUID(user["id"])

    loader = getLoadersFromInfo(info).presencetypes
    row = await loader.update(presence_type)
    result = PresenceTypeResultGQLModel(id=presence_type.id, msg="ok")
    result.msg = "fail" if row is None else "ok"
    return result