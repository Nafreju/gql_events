from typing import List, Union
import typing
import strawberry as strawberryA
import uuid
from contextlib import asynccontextmanager

from .GraphTypeDefinitions import withInfo, getLoaders, EventGQLModel, PresenceGQLModel
###########################################################################################################################
#
# zde definujte sve GQL modely
# - nove, kde mate zodpovednost
# - rozsirene, ktere existuji nekde jinde a vy jim pridavate dalsi atributy
#
###########################################################################################################################
import datetime
from gql_events.GraphResolvers import resolveEventsForUser

from .GraphTypeDefinitions import UserGQLModel, GroupGQLModel
        



from gql_events.GraphResolvers import resolveEventTypeById

@strawberryA.federation.type(keys=["id"], description="""Represents an event type""")
class EventTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).eventtypes
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Name of type (cze)""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Name of type (en)""")
    def name_en(self) -> str:
        return self.name_en

    @strawberryA.field(description="""Related events""")
    async def events(self, info: strawberryA.types.Info) -> List['EventGQLModel']:
        loader = getLoaders(info).event_eventtype_id
        result = await loader.load(self.id)
        return result


@strawberryA.federation.type(keys=["id"], description="""Represents a type of presence (like Present)""")
class PresenceTypeGQLModel:

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).presencetypes
        if id is None:
            return None
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Name of type (cze)""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Name of type (en)""")
    def name_en(self) -> str:
        return self.name_en

@strawberryA.federation.type(keys=["id"], description="""Represents if an user has been invited to the event ot whatever""")
class InvitationTypeGQLModel:

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).invitationtypes
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Name of type (cze)""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Name of type (en)""")
    def name_en(self) -> str:
        return self.name_en




import datetime
from gql_events.GraphResolvers import (
    resolveEventById,
    resolveGroupsForEvent,
    resolvePresencesForEvent
)
    
    # @strawberryA.field(description="""Editor for the event""")
    # async def editor(self, info: strawberryA.types.Info) -> "EventEditorGQLModel":
    #     result = await EventEditorGQLModel.resolve_reference(info=info, id=self.id)
    #     return result

@strawberryA.federation.type(keys=["id"], description="""Entity representing events""")
class EventEditorGQLModel:
    ##
    ## Mutace, obejiti problemu s federativnim API
    ##

    # vysledky opearace update
    id: strawberryA.ID = None
    result: str = None

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = EventEditorGQLModel()
        result.id=id
        result.result="Ok"
        return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Result of update operation""")
    def result(self) -> str:
        return self.result

    @strawberryA.field(description="""Event encapsulated by this editor""")
    async def event(self, info: strawberryA.types.Info) -> EventGQLModel:
        result = await EventGQLModel.resolve_reference(info=info, id=self.id)
        return result

###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################

from typing import Optional
import datetime
from gql_events.GraphResolvers import resolveEventPage, resolveEventTypePage
from sqlalchemy import and_, or_

@strawberryA.type(description="""Type for query root""")
class Query:
    @strawberryA.field(description="""Finds an workflow by their id""")
    async def say_hello_events(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[str, None]:
        result = f"Hello {id}"
        return result

    @strawberryA.field(description="""Finds a particular event""")
    async def event_type_by_id(
        self, info: strawberryA.types.Info, id: uuid.UUID
    ) -> Union[EventTypeGQLModel, None]:
        result = await EventTypeGQLModel.resolve_reference(info, id=id)
        return result

    @strawberryA.field(description="""Finds a particular event""")
    async def event_type_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[EventTypeGQLModel]:
        async with withInfo(info) as session:
            result = await resolveEventTypePage(session, skip=skip, limit=limit)
            return result


    @strawberryA.field(description="""Finds all events paged""")
    async def event_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[EventGQLModel]:
        async with withInfo(info) as session:
            result = await resolveEventPage(session, skip, limit)
            return result

    @strawberryA.field(description="""Finds a particular event""")
    async def event_by_id(
        self, info: strawberryA.types.Info, id: uuid.UUID
    ) -> Union[EventGQLModel, None]:
        result = await EventGQLModel.resolve_reference(info, id=id)
        return result

    @strawberryA.field(description="""Finds all events for an organizer""")
    async def event_by_user(
        self,
        info: strawberryA.types.Info,
        id: strawberryA.ID,
        startdate: Optional[datetime.datetime] = None,
        enddate: Optional[datetime.datetime] = None,
    ) -> List[EventGQLModel]:
        async with withInfo(info) as session:
            result = await resolveEventsForUser(session, id, startdate, enddate)
            return result

    @strawberryA.field(description="""Finds all events for a group""")
    async def event_by_group(
        self,
        info: strawberryA.types.Info,
        id: strawberryA.ID,
        startdate: Optional[datetime.datetime] = None,
        enddate: Optional[datetime.datetime] = None,
    ) -> List[EventGQLModel]:
        async with withInfo(info) as session:
            result = await resolveEventsForGroup(session, id, startdate, enddate)
            return result

    @strawberryA.field(description="""Finds a particular event""")
    async def presence_by_id(
        self, info: strawberryA.types.Info, id: uuid.UUID
    ) -> Union[PresenceGQLModel, None]:
        result = await PresenceGQLModel.resolve_reference(info, id=id)
        return result

    @strawberryA.field(description="""Finds all presences for the event""")
    async def presences_by_event(
        self,
        info: strawberryA.types.Info,
        event_id: strawberryA.ID
    ) -> List[PresenceGQLModel]:
        loader = getLoaders(info).presences
        result = await loader.filter_by(event_id=event_id)
        return result

    @strawberryA.field(description="""Finds all presences for the user in the period""")
    async def presences_by_user(
        self,
        info: strawberryA.types.Info,
        user_id: strawberryA.ID,
        startdate: datetime.datetime,
        enddate: datetime.datetime
    ) -> List[PresenceGQLModel]:
        assert startdate < enddate, "startdate must be sooner than enddate"
        loader = getLoaders(info).presences
        # stmt = loader.getSelectStatement()
        # model = loader.getModel()
        # filterstmt = or_(
        #     and_(model.startdate >= startdate, model.enddate <= startdate),
        #     and_(model.startdate >= enddate, model.enddate <= enddate))
        
        # result = loader.execute_select(stmt.filter(filterstmt))
        result = await loader.filter_by(user_id=user_id)
        return result

    @strawberryA.field(description="""Finds a particular presence type""")
    async def presence_type_by_id(
             self, info: strawberryA.types.Info, id: uuid.UUID
    ) -> Union[PresenceTypeGQLModel, None]:
        result = await PresenceTypeGQLModel.resolve_reference(info, id=id)
        return result


    @strawberryA.field(description="""Returns presence types """)
    async def presence_type_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 20
        
    ) -> List[PresenceTypeGQLModel]:
        loader = getLoaders(info).presencetypes
        result = await loader.page(skip=skip, limit=limit)
        return result
    
    @strawberryA.field(description="""Finds a particular invitation""")
    async def invitation_type_by_id(
             self, info: strawberryA.types.Info, id: uuid.UUID
    ) -> Union[InvitationTypeGQLModel, None]:
        result = await InvitationTypeGQLModel.resolve_reference(info, id=id)
        return result

    @strawberryA.field(description="""Returns invitation types """)
    async def invitation_type_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 20
        
    ) -> List[InvitationTypeGQLModel]:
        loader = getLoaders(info).invitationtypes
        result = await loader.page(skip=skip, limit=limit)
        return result



    # @strawberryA.field(description="""Finds all events for a group""")
    # async def presences_by_user(
    #     self,
    #     info: strawberryA.types.Info,
    #     event_id: strawberryA.ID,
    #     startdate: datetime.datetime,
    #     enddate: datetime.datetime,
    # ) -> List[PresenceGQLModel]:
    #     loader = getLoaders(info).presences
    #     result = loader.filter_by(event_id=event_id)
    #     return result

###########################################################################################################################
#
#
# Mutations
#
#
###########################################################################################################################

from typing import Optional

@strawberryA.input
class EventInsertGQLModel:
    name: str
    eventtype_id: strawberryA.ID
    id: Optional[strawberryA.ID] = None
    masterevent_id: Optional[strawberryA.ID] = None
    startdate: Optional[datetime.datetime] = datetime.datetime.now()
    enddate: Optional[datetime.datetime] = datetime.datetime.now() + datetime.timedelta(minutes = 30)
    pass

@strawberryA.input
class EventUpdateGQLModel:
    id: strawberryA.ID
    lastchange: datetime.datetime
    name: Optional[str] = None
    masterevent_id: Optional[strawberryA.ID] = None
    eventtype_id: Optional[strawberryA.ID] = None
    startdate: Optional[datetime.datetime] = None
    enddate: Optional[datetime.datetime] = None
    
@strawberryA.type
class EventResultGQLModel:
    id: strawberryA.ID = None
    msg: str = None

    @strawberryA.field(description="""Result of user operation""")
    async def event(self, info: strawberryA.types.Info) -> Union[EventGQLModel, None]:
        result = await EventGQLModel.resolve_reference(info, self.id)
        return result
    
@strawberryA.input
class InvitationTypeUpdateGQLModel:
    id: strawberryA.ID
    lastchange: datetime.datetime
    name: Optional[str] = None
    name_en: Optional[str] = None
    created_by: Optional[str] = None
    #changed_by: Optional[str] = None
    
@strawberryA.type
class InvitationTypeResultGQLModel:
    id: strawberryA.ID = None
    msg: str = None

    @strawberryA.field(description="""Result of user operation""")
    async def invitation_types(self, info: strawberryA.types.Info) -> Union[InvitationTypeGQLModel, None]:
        result = await InvitationTypeGQLModel.resolve_reference(info, self.id)
        return result

@strawberryA.input 
class EventTypeUpdateGQLModel:
    id: strawberryA.ID
    lastchange: datetime.datetime
    name: Optional[str] = None
    name_en: Optional[str] = None
    created_by: Optional[str] = None

@strawberryA.type
class EventTypeResultGQLModel:
    id: strawberryA.ID = None
    msg: str = None

    @strawberryA.field(description="""Result of user operation""")
    async def event_types(self, info: strawberryA.types.Info) -> Union[EventTypeGQLModel, None]:
        result = await EventTypeGQLModel.resolve_reference(info, self.id)
        return result
    

@strawberryA.input 
class PresenceTypeUpdateGQLModel:
    id: strawberryA.ID
    lastchange: datetime.datetime
    name: Optional[str] = None
    name_en: Optional[str] = None
    created_by: Optional[str] = None

@strawberryA.type
class PresenceTypeResultGQLModel:
    id: strawberryA.ID = None
    msg: str = None

    @strawberryA.field(description="""Result of user operation""")
    async def presence_types(self, info: strawberryA.types.Info) -> Union[PresenceTypeGQLModel, None]:
        result = await PresenceTypeGQLModel.resolve_reference(info, self.id)
        return result


@strawberryA.input
class PresenceInsertGQLModel:
    user_id: strawberryA.ID
    event_id: strawberryA.ID
    invitation_id: strawberryA.ID
    presencetype_id: Optional[strawberryA.ID] = None
    id: Optional[strawberryA.ID] = None

@strawberryA.input
class PresenceUpdateGQLModel:
    id: strawberryA.ID
    lastchange: datetime.datetime
    invitation_id: Optional[strawberryA.ID] = None
    presencetype_id: Optional[strawberryA.ID] = None
    
@strawberryA.type
class PresenceResultGQLModel:
    id: strawberryA.ID = None
    msg: str = None

    @strawberryA.field(description="""Result of presence operation""")
    async def presence(self, info: strawberryA.types.Info) -> Union[PresenceGQLModel, None]:
        result = await PresenceGQLModel.resolve_reference(info, self.id)
        return result

    
@strawberryA.federation.type(extend=True)
class Mutation:

    @strawberryA.mutation
    async def presence_insert(self, info: strawberryA.types.Info, presence: PresenceInsertGQLModel) -> PresenceResultGQLModel:
        print("presence_insert", presence)
        loader = getLoaders(info).presences
        row = await loader.insert(presence)
        print("presence_insert", row)
        print("presence_insert", row.id)
        result = PresenceResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        return result

    @strawberryA.mutation
    async def presence_update(self, info: strawberryA.types.Info, presence: PresenceUpdateGQLModel) -> PresenceResultGQLModel:
        loader = getLoaders(info).presences
        row = await loader.update(presence)
        result = PresenceResultGQLModel()
        result.msg = "ok"
        result.id = presence.id
        if row is None:
            result.msg = "fail"
            
        return result


    @strawberryA.mutation
    async def event_insert(self, info: strawberryA.types.Info, event: EventInsertGQLModel) -> EventResultGQLModel:
        loader = getLoaders(info).events
        row = await loader.insert(event)
        result = EventResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        return result

    @strawberryA.mutation
    async def event_update(self, info: strawberryA.types.Info, event: EventUpdateGQLModel) -> EventResultGQLModel:
        loader = getLoaders(info).events
        row = await loader.update(event)
        result = EventResultGQLModel()
        result.id = event.id
        result.msg = "ok"  
        if row is None:
            result.msg = "fail"
            
        return result
    
    @strawberryA.mutation
    async def invitation_type_update(self, info: strawberryA.types.Info, invitation_type: InvitationTypeUpdateGQLModel) -> InvitationTypeResultGQLModel: 
        loader = getLoaders(info).invitationtypes
        row = await loader.update(invitation_type)
        result = InvitationTypeResultGQLModel()
        result.id = invitation_type.id
        result.msg = "ok"  
        if row is None:
            result.msg = "fail"
            
        return result
    
    @strawberryA.mutation 
    async def event_type_update(self, info: strawberryA.types.Info, event_type: EventTypeUpdateGQLModel) -> EventTypeResultGQLModel: 
        loader = getLoaders(info).eventtypes
        row = await loader.update(event_type)
        result = EventTypeResultGQLModel()
        result.id = event_type.id
        result.msg = "ok"  
        if row is None:
            result.msg = "fail"
            
        return result
    
    @strawberryA.mutation 
    async def presence_type_update(self, info: strawberryA.types.Info, presence_type: PresenceTypeUpdateGQLModel) -> PresenceTypeResultGQLModel: 
        loader = getLoaders(info).presencetypes
        row = await loader.update(presence_type)
        result = PresenceTypeResultGQLModel()
        result.id = presence_type.id
        result.msg = "ok"  
        if row is None:
            result.msg = "fail"
            
        return result
    

###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

schema = strawberryA.federation.Schema(Query, types=(UserGQLModel,), mutation=Mutation)