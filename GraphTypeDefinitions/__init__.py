import strawberry


from .PresenceGQLModel import PresenceGQLModel
from .EventTypeGQLModel import EventTypeGQLModel
from .PresenceTypeGQLModel import PresenceTypeGQLModel
from .InvitationTypeGQLModel import InvitationTypeGQLModel
from .externals import UserGQLModel, GroupGQLModel
from uuid import UUID
from typing import Optional
from utils.Dataloaders import getUserFromInfo


@strawberry.type(description="""Type for query root""")
class Query:

    @strawberry.field(description="""Say hello world events""")
    async def say_hello_events(self, info: strawberry.types.Info, id: UUID) -> Optional[str]:
        user = getUserFromInfo(info)
        result = f"Hello {id} `{user}`"
        return result

    from .EventGQLModel import event_by_id, event_page
    event_by_id = event_by_id
    event_page = event_page

    from .EventTypeGQLModel import event_type_by_id, event_type_page
    event_type_by_id = event_type_by_id
    event_type_page = event_type_page

    from .InvitationTypeGQLModel import invitation_type_by_id, invitation_type_page
    invitation_type_by_id = invitation_type_by_id
    invitation_type_page = invitation_type_page

    from .PresenceGQLModel import presence_by_id, presence_page
    presence_by_id = presence_by_id
    presence_page = presence_page

    from .PresenceTypeGQLModel import presence_type_by_id, presence_type_page
    presence_type_by_id = presence_type_by_id
    presence_type_page = presence_type_page

    from .EventGroupGQLModel import event_group_by_id, event_group_page
    event_group_by_id = event_group_by_id
    event_group_page = event_group_page

    from .EventCategoryGQLModel import event_category_by_id, event_category_page
    event_category_by_id = event_category_by_id
    event_category_page = event_category_page



@strawberry.type(description="""Type of mutation root""")
class Mutation:
    
    from .EventGQLModel import event_insert, event_update
    event_insert = event_insert
    event_update = event_update

    from .EventTypeGQLModel import event_type_insert, event_type_update
    event_type_insert = event_type_insert
    event_type_update = event_type_update

    from .InvitationTypeGQLModel import invitation_type_insert, invitation_type_update
    invitation_type_insert = invitation_type_insert
    invitation_type_update = invitation_type_update

    from .PresenceGQLModel import presence_insert, presence_update
    presence_insert = presence_insert
    presence_update = presence_update

    from .PresenceTypeGQLModel import presence_type_insert, presence_type_update
    presence_type_insert = presence_type_insert
    presence_type_update = presence_type_update

    from .EventGroupGQLModel import event_group_insert, event_group_delete
    event_group_insert = event_group_insert
    event_group_delete = event_group_delete

    from .EventCategoryGQLModel import event_category_insert, event_category_update
    event_category_insert = event_category_insert
    event_category_update = event_category_update



schema = strawberry.federation.Schema(Query, types=(UserGQLModel, GroupGQLModel), mutation=Mutation)