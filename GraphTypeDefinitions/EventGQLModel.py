import strawberry
import datetime
from typing import List, Annotated, Optional
from ._GraphResolvers import asPage, resolve_result_msg
from utils import getLoadersFromInfo, getUserFromInfo
from uuid import UUID
from dataclasses import dataclass
from uoishelpers.resolvers import createInputs
from .BaseGQLModel import BaseGQLModel
from GraphTypeDefinitions._GraphResolvers import (
    resolve_id,
    resolve_name,
    resolve_name_en,
    resolve_changedby,
    resolve_created,
    resolve_lastchange,
    resolve_createdby,
    resolve_rbacobject,
    asPage
)
from ._GraphPermissions import OnlyForAuthentized

GroupGQLModel = Annotated["GroupGQLModel", strawberry.lazy(".externals")]
EventTypeGQLModel = Annotated["EventTypeGQLModel", strawberry.lazy(".EventTypeGQLModel")]
PresenceGQLModel = Annotated["PresenceGQLModel", strawberry.lazy(".PresenceGQLModel")]

@strawberry.federation.type(
    keys=["id"], description="""Entity representing an event (calendar item)""")
class EventGQLModel(BaseGQLModel):
    
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).events

    id = resolve_id
    name_en = resolve_name_en
    name = resolve_name

    @strawberry.field(description="""Validity of event""",
        permission_classes=[OnlyForAuthentized()])
    def valid(self) -> Optional[bool]:
        return self.valid

    created = resolve_created
    lastchange = resolve_lastchange
    createdby = resolve_createdby
    changedby = resolve_changedby

    @strawberry.field(description="""Date&time of event begin""",
        permission_classes=[OnlyForAuthentized()])
    def startdate(self) -> Optional[datetime.datetime]:
        return self.startdate

    @strawberry.field(description="""Date&time of event end""",
        permission_classes=[OnlyForAuthentized()])
    def enddate(self) -> Optional[datetime.datetime]:
        return self.enddate
    
    rbacobject = resolve_rbacobject
    
    @strawberry.field(description="""Master event of event""",
        permission_classes=[OnlyForAuthentized()])
    def masterevent_id(self) -> Optional[UUID]:
        return self.masterevent_id

    @strawberry.field(description="""Type of event""",
        permission_classes=[OnlyForAuthentized()])
    def eventtype_id(self) -> Optional[UUID]:
        return self.eventtype_id

    @strawberry.field(description="""Groups of users linked to the event""",
        permission_classes=[OnlyForAuthentized(isList=True)])
    async def groups(self, info: strawberry.types.Info) -> List["GroupGQLModel"]:
        loader = getLoadersFromInfo(info).eventgroups
        result = await loader.filter_by(event_id=self.id)
        return result
   
    @strawberry.field(
        description="""Type of the event""",
        permission_classes=[OnlyForAuthentized()])
    async def event_type(self, info: strawberry.types.Info) -> Optional["EventTypeGQLModel"]:
        from .EventTypeGQLModel import EventTypeGQLModel
        result = await EventTypeGQLModel.resolve_reference(info=info, id=self.eventtype_id)
        return result

    @strawberry.field(
        description="""Participants of the event and if they were absent or so...""",
        permission_classes=[OnlyForAuthentized(isList=True)])
    async def presences(self, info: strawberry.types.Info) -> List["PresenceGQLModel"]:
        loader = getLoadersFromInfo(info).presences
        result = await loader.filter_by(event_id=self.id)
        return result 

    @strawberry.field(
        description="""event which contains this event (aka semester of this lesson)""",
        permission_classes=[OnlyForAuthentized()])
    async def master_event(self, info: strawberry.types.Info) -> Optional["EventGQLModel"]:
        return None if self.masterevent_id is None \
                    else await EventGQLModel.resolve_reference(info=info, id=self.masterevent_id)

    @strawberry.field(
        description="""events which are contained by this event (aka all lessons for the semester)""",
        permission_classes=[OnlyForAuthentized(isList=True)])
    async def sub_events(self, info: strawberry.types.Info) -> List["EventGQLModel"]:
        loader = getLoadersFromInfo(info).events
        result = await loader.filter_by(masterevent_id=self.id)
        return result
    
@createInputs
@dataclass
class EventWhereFilter: 
    id: UUID
    name: str
    name_en: str

    valid: bool
    created: datetime.datetime
    createdby: UUID
    changedby: UUID
    startdate: datetime.datetime
    enddate: datetime.datetime
    masterevent_id: UUID
    eventtype_id: UUID

    #TODO eventtype, presences, master_event, sub_events



#Queries

@strawberry.field(
    description="""Finds a particular event""",
        permission_classes=[OnlyForAuthentized()])
async def event_by_id(self, info: strawberry.types.Info, id: UUID) -> Optional[EventGQLModel]:
    result = await EventGQLModel.resolve_reference(info=info, id=id)
    return result



@strawberry.field(
    description="""Finds all events paged""",
        permission_classes=[OnlyForAuthentized(isList=True)])
@asPage
async def event_page(self, info: strawberry.types.Info, skip: int = 0, limit: int = 10, where: Optional[EventWhereFilter] = None) -> List[EventGQLModel]:
    return getLoadersFromInfo(info).events


#Mutations
@strawberry.input(description="Input structure - C operation")
class EventInsertGQLModel:
    name: str = strawberry.field(description="name of event")
    eventtype_id: UUID = strawberry.field(description="type of event")

    id: Optional[UUID] = strawberry.field(description="primary key (UUID), could be client generated", default=None)
    name_en: Optional[str] = strawberry.field(description="name of event in English", default="")

    startdate: Optional[datetime.datetime] = \
        strawberry.field(description="start date of event", default=datetime.datetime.now())
    enddate: Optional[datetime.datetime] = \
        strawberry.field(description="end date of event", default=datetime.datetime.now() + datetime.timedelta(minutes = 30))

    masterevent_id: Optional[UUID] = strawberry.field(description="master event", default=None)
    
    valid: Optional[bool] = True
    createdby: strawberry.Private[UUID] = None
    
@strawberry.input(description="Input structure - UD operation")
class EventUpdateGQLModel:
    id: UUID = strawberry.field(description="primary key (UUID), identifies object of operation")
    lastchange: datetime.datetime = strawberry.field(description="timestamp of last change = TOKEN")

    name: Optional[str] = strawberry.field(description="name of event", default=None)
    name_en: Optional[str] = strawberry.field(description="name of event in English", default=None)

    startdate: Optional[datetime.datetime] = \
        strawberry.field(description="start date of event", default=datetime.datetime.now())
    enddate: Optional[datetime.datetime] = \
        strawberry.field(description="end date of event", default=datetime.datetime.now() + datetime.timedelta(minutes = 30))
    
    masterevent_id: Optional[UUID] = strawberry.field(description="master event", default=None)
    eventtype_id: Optional[UUID] = strawberry.field(description="type of event", default=None)
    
    valid: Optional[bool] = None
    changedby: strawberry.Private[UUID] = None
 
    
@strawberry.type(description="Result of CUD operations")
class EventResultGQLModel:
    id: UUID = strawberry.field(description="primary key of CUD operation object")
    msg: str = strawberry.field(description=\
        """Should be `ok` if descired state has been reached, otherwise `fail`. For update operation fail should be also stated when bad lastchange has been entered.""")

    @strawberry.field(description="""Result of event operation""")
    async def event(self, info: strawberry.types.Info) -> Optional[EventGQLModel]:
        result = await EventGQLModel.resolve_reference(info, self.id)
        return result

@strawberry.mutation(
    description="C operation",
        permission_classes=[OnlyForAuthentized()])
async def event_insert(self, info: strawberry.types.Info, event: EventInsertGQLModel) -> EventResultGQLModel:
    user = getUserFromInfo(info)
    event.createdby = UUID(user["id"])

    loader = getLoadersFromInfo(info).events
    row = await loader.insert(event)
    result = EventResultGQLModel(id=row.id, msg="ok")
    return result


@strawberry.mutation(
    description="U operation",
        permission_classes=[OnlyForAuthentized()])
async def event_update(self, info: strawberry.types.Info, event: EventUpdateGQLModel) -> EventResultGQLModel:
    user = getUserFromInfo(info)
    event.changedby = UUID(user["id"])
    
    loader = getLoadersFromInfo(info).events
    row = await loader.update(event)
    result = EventResultGQLModel(id=event.id, msg="ok")
    result.msg = "fail" if row is None else "ok"
    return result