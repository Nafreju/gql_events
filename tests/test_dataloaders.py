import sqlalchemy
import sys
import asyncio

# setting path
sys.path.append("../gql_events")

import pytest

# from ..uoishelpers.uuid import UUIDColumn

from DBDefinitions import BaseModel
from DBDefinitions import EventModel, EventTypeModel, EventGroupModel
from DBDefinitions import PresenceModel, PresenceTypeModel, InvitationTypeModel

from sqlalchemy.future import select

from shared import prepare_demodata, prepare_in_memory_sqllite, get_demodata


from utils.Dataloaders import createLoaders

@pytest.mark.asyncio
async def test_load_events():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    demodata = get_demodata()
    events = demodata['events']
    event0 = events[0]
    print(event0, flush=True)
    loaders = createLoaders(async_session_maker)
    eventrow = await loaders.events.load(event0['id'])
    
    assert eventrow.id == event0['id']
    assert eventrow.name == event0['name']

@pytest.mark.asyncio
async def test_load_eventtypes():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    demodata = get_demodata()
    events = demodata['eventtypes']
    event0 = events[0]
    print(event0, flush=True)
    loaders = createLoaders(async_session_maker)
    eventrow = await loaders.eventtypes.load(event0['id'])
    
    assert eventrow.id == event0['id']
    assert eventrow.name == event0['name']
