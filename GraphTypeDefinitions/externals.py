import strawberry
import datetime
from typing import List
from .EventGQLModel import EventGQLModel
from .PresenceGQLModel import PresenceGQLModel
from uuid import UUID
from utils import getLoadersFromInfo

from ._GraphResolvers import create_statement_for_user_events, create_statement_for_group_events

@classmethod
async def resolve_reference(cls, info: strawberry.types.Info, id: UUID):
    return cls(id=id)

class BaseEternal:
    id: UUID = strawberry.federation.field(external=True)
    



@strawberry.federation.type(extend=True, keys=["id"])
class UserGQLModel:
    id: UUID = strawberry.federation.field(external=True)
    resolve_reference = resolve_reference

    # TODO dont know how to test it - hunting coverage
    @strawberry.field(description="""Gets events related to the user in the specified interval""")
    async def events(
        self,
        info: strawberry.types.Info,
        startdate: datetime.datetime = None,
        enddate: datetime.datetime = None,
    ) -> List["EventGQLModel"]:
        statement = create_statement_for_user_events(self.id, startdate=startdate, enddate=enddate)
        loader = getLoadersFromInfo(info).events
        result = await loader.execute_select(statement)
        return result

    # TODO dont know how to test it - hunting coverage
    # @strawberry.field(description="""pass""")
    # async def presencies(
    #     self, info
    # ) -> List["PresenceGQLModel"]:
    #     loader = getLoadersFromInfo(info).presences
    #     result = await loader.filter_by(user_id=self.id)
    #     return result


@strawberry.federation.type(extend=True, keys=["id"])
class GroupGQLModel:
    id: UUID = strawberry.federation.field(external=True)
    resolve_reference = resolve_reference

    # TODO dont know how to test it - hunting coverage
    @strawberry.field(description="""Events related to a group""")
    async def events(
        self,
        info: strawberry.types.Info,
        startdate: datetime.datetime = None,
        enddate: datetime.datetime = None,
        # eventtype_id: UUID = None
    ) -> List["EventGQLModel"]:
        statement = create_statement_for_group_events(self.id, startdate=startdate, enddate=enddate)
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