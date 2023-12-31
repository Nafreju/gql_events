import strawberry
import datetime
from typing import List
from .utils import withInfo, getLoaders
from .EventGQLModel import EventGQLModel
from .PresenceGQLModel import PresenceGQLModel
from uuid import UUID

from GraphResolvers import resolveEventsForGroup, resolveEventsForUser, create_statement_for_user_events


@strawberry.federation.type(extend=True, keys=["id"])
class UserGQLModel:

    id: UUID = strawberry.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: UUID):
        return UserGQLModel(id=id)

    @strawberry.field(description="""Gets events related to the user in the specified interval""")
    async def events(
        self,
        info: strawberry.types.Info,
        startdate: datetime.datetime = None,
        enddate: datetime.datetime = None,
    ) -> List["EventGQLModel"]:
        statement = create_statement_for_user_events(self.id, startdate=startdate, enddate=enddate)
        loader = getLoaders(info).events
        result = await loader.execute_select(statement)
        return result
        
    @strawberry.field(description="""pass""")
    async def presencies(
        self, info
    ) -> List["PresenceGQLModel"]:
        loader = getLoaders(info).presences
        result = await loader.filter_by(user_id=self.id)
        return result


#TODO events function
@strawberry.federation.type(extend=True, keys=["id"])
class GroupGQLModel:

    id: UUID = strawberry.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: UUID):
        return GroupGQLModel(id=id)

    @strawberry.field(description="""Events related to a group""")
    async def events(
        self,
        info: strawberry.types.Info,
        startdate: datetime.datetime = None,
        enddate: datetime.datetime = None,
        # eventtype_id: strawberry.ID = None
    ) -> List["EventGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveEventsForGroup(session, self.id, startdate, enddate)
            return result