import strawberry
import datetime
from typing import Union, List, Annotated, Optional
from .utils import withInfo, getLoaders

from uuid import UUID

GroupGQLModel = Annotated["GroupGQLModel", strawberry.lazy(".externals")]
EventTypeGQLModel = Annotated["EventTypeGQLModel", strawberry.lazy(".EventTypeGQLModel")]
PresenceGQLModel = Annotated["PresenceGQLModel", strawberry.lazy(".PresenceGQLModel")]

@strawberry.federation.type(keys=["id"], description="""Entity representing an event (calendar item)""")
class EventGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: UUID):
        eventsloader = getLoaders(info).events
        result = await eventsloader.load(id)
        if result is not None:
            result.__strawberry_definition__ = cls.__strawberry_definition__  # little hack :)
        return result

    @strawberry.field(description="""Primary key""")
    def id(self) -> UUID:
        return self.id

    @strawberry.field(description="""Time stamp""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberry.field(description="""Event name in Czech""")
    def name(self) -> Union[str, None]:
        return self.name
    
    @strawberry.field(description="""Event name in English""")
    def name_en(self) -> Union[str, None]:
        return self.name

    @strawberry.field(description="""Date&time of event begin""")
    def startdate(self) -> Union[datetime.datetime, None]:
        return self.startdate

    @strawberry.field(description="""Date&time of event end""")
    def enddate(self) -> Union[datetime.datetime, None]:
        return self.enddate

    @strawberry.field(description="""Groups of users linked to the event""")
    async def groups(self, info: strawberry.types.Info) -> List["GroupGQLModel"]:
        async with withInfo(info) as session:
            pass
            #links = await resolveGroupsForEvent(session, self.id)
            # result = list(map(lambda item: GroupGQLModel(id=item.group_id), links))
            # return result
            #return map(lambda item: GroupGQLModel(id=item.group_id), links)
            


    @strawberry.field(description="""Participants of the event and if they were absent or so...""")
    async def presences(self, info: strawberry.types.Info, invitation_types: List[strawberry.ID] = []) -> List["PresenceGQLModel"]:
        async with withInfo(info) as session:
            #result = await resolvePresencesForEvent(session, self.id, invitation_types)
            #return result
            pass

    @strawberry.field(description="""Type of the event""")
    async def event_type(self, info: strawberry.types.Info) -> Optional["EventTypeGQLModel"]:
        result = await EventTypeGQLModel.resolve_reference(info=info, id=self.eventtype_id)
        return result

    @strawberry.field(description="""event which contains this event (aka semester of this lesson)""")
    async def master_event(self, info: strawberry.types.Info) -> Optional["EventGQLModel"]:
        if (self.masterevent_id is None):
            result = None
        else:
            result = await EventGQLModel.resolve_reference(info=info, id=self.masterevent_id)
        return result

    @strawberry.field(description="""events which are contained by this event (aka all lessons for the semester)""")
    async def sub_events(self, info: strawberry.types.Info, startdate: datetime.datetime, enddate: datetime.datetime) -> List["EventGQLModel"]:
        loader = getLoaders(info).events
        #TODO
        result = await loader.filter_by(masterevent_id=self.id)
        return result

#Queries
@strawberry.field(description="""Finds a particular event""")
async def event_by_id(self, info: strawberry.types.Info, id: UUID) -> Optional[EventGQLModel]:
    result = await EventGQLModel.resolve_reference(info, id=id)
    return result

@strawberry.field(description="""Finds all events paged""")
async def event_page(self, info: strawberry.types.Info, skip: int = 0, limit: int = 10) -> List[EventGQLModel]:
    loader = getLoaders(info).events
    result = await loader.page(skip, limit)
    return result


@strawberry.input
class EventInsertGQLModel:
    name: str
    eventtype_id: strawberry.ID
    id: Optional[strawberry.ID] = None
    masterevent_id: Optional[strawberry.ID] = None
    startdate: Optional[datetime.datetime] = datetime.datetime.now()
    enddate: Optional[datetime.datetime] = datetime.datetime.now() + datetime.timedelta(minutes = 30)
    pass

@strawberry.input
class EventUpdateGQLModel:
    id: strawberry.ID
    lastchange: datetime.datetime
    name: Optional[str] = None
    masterevent_id: Optional[strawberry.ID] = None
    eventtype_id: Optional[strawberry.ID] = None
    startdate: Optional[datetime.datetime] = None
    enddate: Optional[datetime.datetime] = None
    
@strawberry.type
class EventResultGQLModel:
    id: strawberry.ID = None
    msg: str = None

    @strawberry.field(description="""Result of user operation""")
    async def event(self, info: strawberry.types.Info) -> Union[EventGQLModel, None]:
        result = await EventGQLModel.resolve_reference(info, self.id)
        return result
    

#Mutations
@strawberry.mutation
async def event_insert(self, info: strawberry.types.Info, event: EventInsertGQLModel) -> EventResultGQLModel:
    loader = getLoaders(info).events
    row = await loader.insert(event)
    result = EventResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result


@strawberry.mutation
async def event_update(self, info: strawberry.types.Info, event: EventUpdateGQLModel) -> EventResultGQLModel:
    loader = getLoaders(info).events
    row = await loader.update(event)
    result = EventResultGQLModel()
    result.id = event.id
    result.msg = "ok"  
    if row is None:
        result.msg = "fail"
        
    return result