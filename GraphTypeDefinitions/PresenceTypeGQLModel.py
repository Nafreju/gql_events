import strawberry
import datetime
from typing import Union, List, Annotated, Optional
from .utils import withInfo, getLoaders, getUser
from uuid import UUID

PresenceGQLModel = Annotated["PresenceGQLModel", strawberry.lazy(".PresenceGQLModel")]


@strawberry.federation.type(keys=["id"], description="""Represents a type of presence (like Present)""")
class PresenceTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: UUID):
        loader = getLoaders(info).presencetypes

        result = await loader.load(id)
        if result is not None:
            result.__strawberry_definition__ = cls.__strawberry_definition__  # little hack :)
        return result

    @strawberry.field(description="""Primary key""")
    def id(self) -> UUID:
        return self.id

    @strawberry.field(description="""Name of presence type""")
    def name(self) -> Optional[str]:
        return self.name

    @strawberry.field(description="""Name of presence type in English""")
    def name_en(self) -> Optional[str]:
        return self.name_en

    @strawberry.field(description="""Validity of presence type""")
    def valid(self) -> Optional[bool]:
        return self.valid
    
    @strawberry.field(description="""When presence type was created""")
    def created(self) -> Optional[datetime.datetime]:
        return self.created

    @strawberry.field(description="""Time stamp""")
    def lastchange(self) -> Optional[datetime.datetime]:
        return self.lastchange
    
    @strawberry.field(description="""By whom presence type was created""")
    def createdby(self) -> Optional[UUID]:
        return self.createdby

    @strawberry.field(description="""Who changed the presence type""")
    def changedby(self) -> Optional[UUID]:
        return self.changedby
   
   #TODO resolve RBACObject


    @strawberry.field(description="Presences who have this presence type")
    async def presences(self, info: strawberry.types.Info) -> Optional[List[PresenceGQLModel]]:
        loader = getLoaders(info).presences
        result = await loader.filter_by(presencetype_id=self.id)
        return result



#Queries
@strawberry.field(description="""Finds a particular presence type""")
async def presence_type_by_id(self, info: strawberry.types.Info, id: UUID) -> Optional[PresenceTypeGQLModel]:
    result = await PresenceTypeGQLModel.resolve_reference(info=info, id=id)
    return result

@strawberry.field(description="""Finds all presence types paged""")
async def presence_type_page(self, info: strawberry.types.Info, skip: int = 0, limit: int = 10) -> Optional[List[PresenceTypeGQLModel]]:
    loader = getLoaders(info).presencetypes
    result = await loader.page(skip, limit)
    return result


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
    

    
@strawberry.mutation(description="C operation")
async def presence_type_insert(self, info: strawberry.types.Info, presence_type: PresenceTypeInsertGQLModel) -> PresenceTypeResultGQLModel:
    user = getUser(info) #TODO
    #event.changedby = UUID(user["id"])

    loader = getLoaders(info).presencetypes
    row = await loader.insert(presence_type)
    result = PresenceTypeResultGQLModel(id=row.id, msg="ok")
    return result

@strawberry.mutation(description="U operation")
async def presence_type_update(self, info: strawberry.types.Info, presence_type: PresenceTypeUpdateGQLModel) -> PresenceTypeResultGQLModel:
    user = getUser(info) #TODO
    #event.changedby = UUID(user["id"])

    loader = getLoaders(info).presencetypes
    row = await loader.update(presence_type)
    result = PresenceTypeResultGQLModel(id=presence_type.id, msg="ok")
    result.msg = "fail" if row is None else "ok"
    return result