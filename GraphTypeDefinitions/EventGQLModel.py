import strawberry
import datetime
from typing import Union, List, Annotated, Optional
from .utils import withInfo, getLoaders, getUser

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

    @strawberry.field(description="""Event name in Czech""")
    def name(self) -> Optional[str]:
        return self.name
    
    @strawberry.field(description="""Event name in English""")
    def name_en(self) -> Optional[str]:
        return self.name

    @strawberry.field(description="""Validity of event""")
    def valid(self) -> Optional[bool]:
        return self.valid
    
    @strawberry.field(description="""When event was created""")
    def created(self) -> Optional[datetime.datetime]:
        return self.created

    @strawberry.field(description="""Time stamp""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange
    
    @strawberry.field(description="""By whom event was created""")
    def createdby(self) -> Optional[UUID]:
        return self.createdby

    @strawberry.field(description="""Who changed the event""")
    def changedby(self) -> Optional[UUID]:
        return self.changedby
    
    @strawberry.field(description="""Date&time of event begin""")
    def startdate(self) -> Optional[datetime.datetime]:
        return self.startdate

    @strawberry.field(description="""Date&time of event end""")
    def enddate(self) -> Optional[datetime.datetime]:
        return self.enddate
    
    @strawberry.field(description="""Master event of event""")
    def masterevent_id(self) -> Optional[UUID]:
        return self.masterevent_id

    @strawberry.field(description="""Type of event""")
    def eventtype_id(self) -> Optional[UUID]:
        return self.eventtype_id
    
    #TODO resolve RBACObject

    @strawberry.field(description="""Groups of users linked to the event""")
    async def groups(self, info: strawberry.types.Info) -> List["GroupGQLModel"]:
        pass
        """
        loader = getLoaders(info).eventgroups
        result = await loader.filter_by(event_id=self.id)
        return result
        """

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
        if self.masterevent_id is None:
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

#Mutations
@strawberry.input(description="Input structure - C operation")
class EventInsertGQLModel:
    name: str = strawberry.field(description="name of event")
    eventtype_id: UUID = strawberry.field(description="type of event")

    id: Optional[UUID] = strawberry.field(description="primary key (UUID), could be client generated", default=None)
    name_en: Optional[str] = strawberry.field(description="name of event in English", default=None)

    startdate: Optional[datetime.datetime] = \
        strawberry.field(description="start date of event", default=datetime.datetime.now())
    enddate: Optional[datetime.datetime] = \
        strawberry.field(description="end date of event", default=datetime.datetime.now() + datetime.timedelta(minutes = 30))

    masterevent_id: Optional[UUID] = strawberry.field(description="master event", default=None)
    
    valid: Optional[bool] = True
    createdby: strawberry.Private[UUID] = None
    
@strawberry.input(description="Input structure - UD operation")
class EventUpdateGQLModel:
    id: UUID = strawberry.field(description="primary key (UUID), could be client generated")
    lastchange: datetime.datetime = strawberry.field(description="timestamp of last change = TOKEN")

    name: Optional[str] = strawberry.field(description="name of event", default=None)
    name_en: Optional[str] = strawberry.field(description="name of event in English", default=None)

    startdate: Optional[datetime.datetime] = \
        strawberry.field(description="start date of event", default=datetime.datetime.now())
    enddate: Optional[datetime.datetime] = \
        strawberry.field(description="end date of event", default=datetime.datetime.now() + datetime.timedelta(minutes = 30))
    
    masterevent_id: Optional[UUID] = strawberry.field(description="master event", default=None)
    eventtype_id: Optional[strawberry.ID] = strawberry.field(description="type of event", default=None)
    
    valid: Optional[bool] = strawberry.field(description="validity of event")
    changedby: strawberry.Private[UUID] = None
 
    
@strawberry.type(description="Result of CU operations")
class EventResultGQLModel:
    id: UUID = strawberry.field(description="primary key of CU operation object")
    msg: str = strawberry.field(description=\
        """Should be `ok` if descired state has been reached, otherwise `fail`. For update operation fail should be also stated when bad lastchange has been entered.""")

    @strawberry.field(description="""Result of event operation""")
    async def event(self, info: strawberry.types.Info) -> Union[EventGQLModel, None]:
        result = await EventGQLModel.resolve_reference(info, self.id)
        return result

@strawberry.mutation(description="C operation")
async def event_insert(self, info: strawberry.types.Info, event: EventInsertGQLModel) -> EventResultGQLModel:
    user = getUser(info) #TODO
    #event.changedby = UUID(user["id"])

    loader = getLoaders(info).events
    row = await loader.insert(event)
    result = EventResultGQLModel(id=row.id, msg="ok")
    return result


@strawberry.mutation(description="U operation")
async def event_update(self, info: strawberry.types.Info, event: EventUpdateGQLModel) -> EventResultGQLModel:
    user = getUser(info) #TODO
    #event.changedby = UUID(user["id"])

    loader = getLoaders(info).events
    row = await loader.update(event)
    result = EventResultGQLModel(id=row.id, msg="ok")
    result.msg = "fail" if row is None else "ok"
    return result