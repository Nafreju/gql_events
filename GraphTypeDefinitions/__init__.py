import strawberry

from .utils import withInfo, getLoaders
from .PresenceGQLModel import PresenceGQLModel
from .EventTypeGQLModel import EventTypeGQLModel
from .PresenceTypeGQLModel import PresenceTypeGQLModel
from .InvitationTypeGQLModel import InvitationTypeGQLModel
from .StateExamGQLModel import StateExamGQLModel
from .externals import UserGQLModel, GroupGQLModel
from uuid import UUID
from typing import Optional









@strawberry.type(description="""Type for query root""")
class Query:

    @strawberry.field(description="""Say hello world events""")
    async def say_hello_events(self, info: strawberry.types.Info, id: strawberry.ID) -> Optional[str]:
        result = f"Hello {id}"
        return result

    from .EventGQLModel import event_by_id, event_page
    event_by_id = event_by_id
    event_page = event_page

    from .EventTypeGQLModel import event_type_by_id, event_type_page
    event_type_by_id = event_type_by_id
    event_type_page = event_type_page


@strawberry.type(description="""Type of mutation root""")
class Mutation:
    
    from .EventGQLModel import event_insert, event_update
    event_insert = event_insert
    event_update = event_update



















schema = strawberry.federation.Schema(Query, types=(UserGQLModel, GroupGQLModel), mutation=Mutation)