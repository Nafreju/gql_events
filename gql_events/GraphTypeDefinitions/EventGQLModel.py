import strawberry as strawberryA
import datetime
from typing import Union, List, Annotated, Optional
from .utils import withInfo, getLoaders
from ..GraphResolvers import resolveGroupsForEvent, resolvePresencesForEvent


GroupGQLModel = Annotated["GroupGQLModel", strawberryA.lazy(".externals")]
EventTypeGQLModel = Annotated["EventTypeGQLModel", strawberryA.lazy("..GraphTypeDefinitionsOld")]
PresenceGQLModel = Annotated["PresenceGQLModel", strawberryA.lazy(".PresenceGQLModel")]

@strawberryA.federation.type(keys=["id"], description="""Entity representing an event (calendar item)""")
class EventGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        eventsloader = getLoaders(info).events
        result = await eventsloader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Time stamp""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""Event name in Czech""")
    def name(self) -> Union[str, None]:
        return self.name
    
    @strawberryA.field(description="""Event name in English""")
    def name_en(self) -> Union[str, None]:
        return self.name

    @strawberryA.field(description="""Date&time of event begin""")
    def startdate(self) -> Union[datetime.datetime, None]:
        return self.startdate

    @strawberryA.field(description="""Date&time of event end""")
    def enddate(self) -> Union[datetime.datetime, None]:
        return self.enddate

    @strawberryA.field(description="""Groups of users linked to the event""")
    async def groups(self, info: strawberryA.types.Info) -> List["GroupGQLModel"]:
        async with withInfo(info) as session:
            links = await resolveGroupsForEvent(session, self.id)
            # result = list(map(lambda item: GroupGQLModel(id=item.group_id), links))
            # return result
            return map(lambda item: GroupGQLModel(id=item.group_id), links)
            


    @strawberryA.field(description="""Participants of the event and if they were absent or so...""")
    async def presences(self, info: strawberryA.types.Info, invitation_types: List[strawberryA.ID] = []) -> List["PresenceGQLModel"]:
        async with withInfo(info) as session:
            result = await resolvePresencesForEvent(session, self.id, invitation_types)
            return result

    @strawberryA.field(description="""Type of the event""")
    async def event_type(self, info: strawberryA.types.Info) -> Optional["EventTypeGQLModel"]:
        result = await EventTypeGQLModel.resolve_reference(info=info, id=self.eventtype_id)
        return result

    @strawberryA.field(description="""event which contains this event (aka semester of this lesson)""")
    async def master_event(self, info: strawberryA.types.Info) -> Optional["EventGQLModel"]:
        if (self.masterevent_id is None):
            result = None
        else:
            result = await EventGQLModel.resolve_reference(info=info, id=self.masterevent_id)
        return result

    @strawberryA.field(description="""events which are contained by this event (aka all lessons for the semester)""")
    async def sub_events(self, info: strawberryA.types.Info, startdate: datetime.datetime, enddate: datetime.datetime) -> List["EventGQLModel"]:
        loader = getLoaders(info).events
        #TODO
        result = await loader.filter_by(masterevent_id=self.id)
        return result