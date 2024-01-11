import strawberry
import datetime
from typing import Union, List, Annotated, Optional
from .utils import withInfo
from utils import getLoadersFromInfo

from uuid import UUID


UserGQLModel = Annotated["UserGQLModel", strawberry.lazy(".externals")]
EventGQLModel = Annotated["EventGQLModel", strawberry.lazy(".EventGQLModel")]
EventTypeGQLModel = Annotated["EventTypeGQLModel", strawberry.lazy(".EventTypeGQLModel")]
GroupGQLModel = Annotated["GroupGQLModel", strawberry.lazy(".GroupGQLModel")]

PresenceTypeGQLModel = Annotated["PresenceTypeGQLModel", strawberry.lazy(".PresenceTypeGQLModel")]
InvitationTypeGQLModel = Annotated["InvitationTypeGQLModel", strawberry.lazy(".InvitationTypeGQLModel")]

@strawberry.federation.type(keys=["id"], description="""Entity representing an state exam""")
class StateExamGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: UUID):
        state_exam_loader = getLoadersFromInfo(info).stateexams
        result = await state_exam_loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  
        return result

    @strawberry.field(description="""Primary key""")
    def id(self) -> UUID:
        return self.id

    @strawberry.field(description="""Time stamp""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberry.field(description="""Event name""")
    def name(self) -> Union[str, None]:
        return self.name
    
    @strawberry.field(description="""Event name in English""")
    def name_en(self) -> Optional[str]:
        return self.name
    
    @strawberry.field(description="""Validity of event""")
    def valid(self) -> Optional[bool]:
        return self.valid

    @strawberry.field(description="""Date&time of event begin""")
    def startdate(self) -> Union[datetime.datetime, None]:
        return self.startdate

    @strawberry.field(description="""Date&time of event end""")
    def enddate(self) -> Union[datetime.datetime, None]:
        return self.enddate
    
    """ @strawberry.field(description="Invited, Accepted, etc.")
    async def invitation_type(self, info: strawberry.types.Info) -> Optional["InvitationTypeGQLModel"]:
        result = await InvitationTypeGQLModel.resolve_reference(info, self.invitation_id)
        return result"""
    
    @strawberry.field(description="""The user / participant""")
    def user(self) -> Optional["UserGQLModel"]:
        result = UserGQLModel(id=self.user_id)
        return result
    

    @strawberry.field(description="""The event""")
    async def event(self, info: strawberry.types.Info) -> Optional["EventGQLModel"]:
        result = await EventGQLModel.resolve_reference(info, id=self.event_id)
        return result
    
    @strawberry.field(description="""Groups of users linked to the event""")
    async def groups(self, info: strawberry.types.Info) -> List["GroupGQLModel"]:
        pass
        """
        loader = getLoaders(info).eventgroups
        result = await loader.filter_by(event_id=self.id)
        return result
        """

    @strawberry.field(description="""By whom event was created""")
    def createdby(self) -> Optional[UUID]:
        return self.createdby

    @strawberry.field(description="""Who changed the event""")
    def changedby(self) -> Optional[UUID]:
        return self.changedby
    
    @strawberry.field(description="""When event was created""")
    def created(self) -> Optional[datetime.datetime]:
        return self.created
    
    #Queries
   
  
    #Mutations
