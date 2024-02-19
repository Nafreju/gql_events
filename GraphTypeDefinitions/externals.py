import strawberry
import datetime
from typing import List, Optional
from .EventGQLModel import EventGQLModel
from .PresenceGQLModel import PresenceGQLModel
from uuid import UUID
from utils import getLoadersFromInfo


@classmethod
async def resolve_reference(cls, info: strawberry.types.Info, id: UUID):
    return cls(id=id)

class BaseEternal:
    id: UUID = strawberry.federation.field(external=True)
    

from ._GraphResolvers import create_statement_for_user_events, create_statement_for_group_events
from dataclasses import dataclass
from uoishelpers.resolvers import createInputs

@createInputs
@dataclass
class UserGroupEventInputFilter:
    name: str
    name_en: str

    valid: bool
    created: datetime.datetime
    createdby: UUID
    changedby: UUID
    startdate: datetime.datetime
    enddate: datetime.datetime
    masterevent_id: UUID
    eventtype_id: UUID
 
    from .EventTypeGQLModel import EventTypeWhereFilter
    eventtype: EventTypeWhereFilter


@strawberry.federation.type(extend=True, keys=["id"])
class UserGQLModel:
    id: UUID = strawberry.federation.field(external=True)
    resolve_reference = resolve_reference

    @strawberry.field(description="""Gets events related to the user in the specified interval""")
    async def events(
        self,
        info: strawberry.types.Info,
        skip: Optional[int] = 0,
        limit: Optional[int] = 10,
        where: Optional[UserGroupEventInputFilter] = None
    ) -> List["EventGQLModel"]:
        wheredict = None if where is None else strawberry.asdict(where)
        statement = create_statement_for_user_events(self.id, where=wheredict)
        statement = statement.offset(skip).limit(limit)
        loader = getLoadersFromInfo(info).events
        result = await loader.execute_select(statement)
        return result



@strawberry.federation.type(extend=True, keys=["id"])
class GroupGQLModel:
    id: UUID = strawberry.federation.field(external=True)
    resolve_reference = resolve_reference

    @strawberry.field(description="""Events related to a group""")
    async def events(
        self,
        info: strawberry.types.Info,
        skip: Optional[int] = 0,
        limit: Optional[int] = 10,
        where: Optional[UserGroupEventInputFilter] = None
    ) -> List["EventGQLModel"]:
        wheredict = None if where is None else strawberry.asdict(where)
        statement = create_statement_for_group_events(self.id, where=wheredict)
        statement = statement.offset(skip).limit(limit)
        loader = getLoadersFromInfo(info).events
        result = await loader.execute_select(statement)
        return result
        


@strawberry.federation.type(extend=True, keys=["id"])
class RBACObjectGQLModel:
    id: UUID = strawberry.federation.field(external=True)
    resolve_reference = resolve_reference

    @classmethod
    async def resolve_roles(cls, info: strawberry.types.Info, id: UUID):
        loader = getLoadersFromInfo(info).authorizations
        authorizedroles = await loader.load(id)
        return authorizedroles