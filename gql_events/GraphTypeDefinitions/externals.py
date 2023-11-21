import strawberry as strawberryA
import datetime
from typing import List
from .utils import withInfo, getLoaders
from .EventGQLModel import EventGQLModel
from .PresenceGQLModel import PresenceGQLModel

from gql_events.GraphResolvers import resolveEventsForGroup, resolveEventsForUser



@strawberryA.federation.type(extend=True, keys=["id"])
class UserGQLModel:

    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberryA.ID):
        return UserGQLModel(id=id)

    @strawberryA.field(description="""Gets events related to the user in the specified interval""")
    async def events(
        self,
        info: strawberryA.types.Info,
        startdate: datetime.datetime = None,
        enddate: datetime.datetime = None,
    ) -> List["EventGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveEventsForUser(session, self.id, startdate, enddate)
            return result
        
    @strawberryA.field(description="""pass""")
    async def presencies(
        self, info
    ) -> List["PresenceGQLModel"]:
        loader = getLoaders(info).presences
        result = await loader.filter_by(user_id=self.id)
        return result

@strawberryA.federation.type(extend=True, keys=["id"])
class GroupGQLModel:

    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberryA.ID):
        return GroupGQLModel(id=id)

    @strawberryA.field(description="""Events related to a group""")
    async def events(
        self,
        info: strawberryA.types.Info,
        startdate: datetime.datetime = None,
        enddate: datetime.datetime = None,
        # eventtype_id: strawberryA.ID = None
    ) -> List["EventGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveEventsForGroup(session, self.id, startdate, enddate)
            return result