import strawberry
import datetime
from typing import Union, List, Annotated, Optional
from .utils import getLoaders


UserGQLModel = Annotated["UserGQLModel", strawberry.lazy(".externals")]
PresenceTypeGQLModel = Annotated["PresenceTypeGQLModel", strawberry.lazy(".PresenceTypeGQLModel")]
InvitationTypeGQLModel = Annotated["InvitationTypeGQLModel", strawberry.lazy(".InvitationTypeGQLModel")]
EventGQLModel = Annotated["EventGQLModel", strawberry.lazy(".EventGQLModel")]

@strawberry.federation.type(keys=["id"], description="""Describes a relation of an user to the event by invitation (like invited) and participation (like absent)""")
class PresenceGQLModel:

    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: strawberry.ID):
        if id is None:
            return None
        loader = getLoaders(info).presences
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberry.field(description="""Primary key""")
    def id(self) -> strawberry.ID:
        return self.id

    @strawberry.field(description="""Time stamp""")
    def lastchange(self) -> Union[datetime.datetime, None]:
        return self.lastchange

    @strawberry.field(description="""Present, Vacation etc.""")
    async def presence_type(self, info: strawberry.types.Info) -> Optional["PresenceTypeGQLModel"]:
        result = await PresenceTypeGQLModel.resolve_reference(info, self.presencetype_id)
        return result

    @strawberry.field(description="""Invited, Accepted, etc.""")
    async def invitation_type(self, info: strawberry.types.Info) -> Optional["InvitationTypeGQLModel"]:
        result = await InvitationTypeGQLModel.resolve_reference(info, self.invitation_id)
        return result

    @strawberry.field(description="""The user / participant""")
    def user(self) -> Optional["UserGQLModel"]:
        result = UserGQLModel(id=self.user_id)
        return result

    @strawberry.field(description="""The event""")
    async def event(self, info: strawberry.types.Info) -> Optional["EventGQLModel"]:
        result = await EventGQLModel.resolve_reference(info, id=self.event_id)
        return result