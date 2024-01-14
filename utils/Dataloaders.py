from functools import cache
import logging

from DBDefinitions import (
    EventModel, 
    EventTypeModel, 
    EventCategoryModel,
    EventGroupModel, 
    PresenceModel,
    InvitationTypeModel, 
    PresenceTypeModel
)


dbmodels = {
    "events": EventModel, 
    "eventtypes": EventTypeModel, 
    "eventcategories": EventCategoryModel,
    "events_groups": EventGroupModel, 
    "events_users": PresenceModel,
    "eventinvitationtypes": InvitationTypeModel, 
    "eventpresencetypes": PresenceTypeModel
}

import datetime
import aiohttp
import asyncio
import os
from aiodataloader import DataLoader
from uoishelpers.resolvers import select, update, delete
from uoishelpers.dataloaders import createIdLoader

@cache
def composeAuthUrl():
    hostname = os.environ.get("GQLUG_ENDPOINT_URL", None)
    assert hostname is not None, "undefined GQLUG_ENDPOINT_URL"
    assert "://" in hostname, "probably bad formated url, has it 'protocol' part?"
    assert "." not in hostname, "security check failed, change source code"
    return hostname

class AuthorizationLoader(DataLoader):

    query = """query($id: UUID!){result: rbacById(id: $id) {roles {user { id } group { id } roletype { id }}}}"""
            # variables = {"id": rbacobject}

    roleUrlEndpoint=None#composeAuthUrl()
    def __init__(self,
        roleUrlEndpoint=roleUrlEndpoint,
        query=query,
        demo=True):
        super().__init__(cache=True)
        self.roleUrlEndpoint = roleUrlEndpoint if roleUrlEndpoint else composeAuthUrl()
        self.query = query
        self.demo = demo
        self.authorizationToken = ""

    def setTokenByInfo(self, info):
        self.authorizationToken = ""

    async def _load(self, id):
        variables = {"id": f"{id}"}
        if self.authorizationToken != "":
            headers = {"authorization": f"Bearer {self.authorizationToken}"}
        else:
            headers = {}
        json = {
            "query": self.query,
            "variables": variables
        }
        roleUrlEndpoint=self.roleUrlEndpoint
        async with aiohttp.ClientSession() as session:
            print(f"query {roleUrlEndpoint} for json={json}")
            async with session.post(url=roleUrlEndpoint, json=json, headers=headers) as resp:
                print(resp.status)
                if resp.status != 200:
                    text = await resp.text()
                    print(text)
                    return []
                else:
                    respJson = await resp.json()

        # print(20*"respJson")
        # print(respJson)
        
        assert respJson.get("errors", None) is None, respJson["errors"]
        respdata = respJson.get("data", None)
        assert respdata is not None, "missing data response"
        result = respdata.get("result", None)
        assert result is not None, "missing result"
        roles = result.get("roles", None)
        assert roles is not None, "missing roles"
        
        # print(30*"=")
        # print(roles)
        # print(30*"=")
        return [*roles]


    async def batch_load_fn(self, keys):
        #print('batch_load_fn', keys, flush=True)
        reducedkeys = set(keys)
        awaitables = (self._load(key) for key in reducedkeys)
        results = await asyncio.gather(*awaitables)
        indexedResult = {key:result for key, result in zip(reducedkeys, results)}
        results = [indexedResult[key] for key in keys]
        return results
    
class Loaders:
    events = None
    eventtypes = None
    eventcategories = None
    presences = None
    invitationtypes = None
    presencetypes = None
    eventgroups = None
    pass

def createLoaders(asyncSessionMaker):

    class Loaders:

        @property
        @cache
        def authorizations(self):
            return AuthorizationLoader()
    
        @property
        @cache
        def events(self):
            return createIdLoader(asyncSessionMaker, EventModel)

        @property
        @cache
        def eventtypes(self):
            return createIdLoader(asyncSessionMaker, EventTypeModel)

        @property
        @cache
        def eventcategories(self):
            return createIdLoader(asyncSessionMaker, EventCategoryModel)

        @property
        @cache
        def presences(self):
            return createIdLoader(asyncSessionMaker, PresenceModel)

        @property
        @cache
        def invitationtypes(self):
            return createIdLoader(asyncSessionMaker, InvitationTypeModel)

        @property
        @cache
        def presencetypes(self):
            return createIdLoader(asyncSessionMaker, PresenceTypeModel)

        @property
        @cache
        def eventgroups(self):
            return createIdLoader(asyncSessionMaker, EventGroupModel)
        
    return Loaders()

def getLoadersFromInfo(info):
    context = info.context
    loaders = context["loaders"]
    return loaders



demouser = {
    "id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003",
    "name": "John",
    "surname": "Newbie",
    "email": "john.newbie@world.com",
    "roles": [
        {
            "valid": True,
            "group": {
                "id": "2d9dcd22-a4a2-11ed-b9df-0242ac120003",
                "name": "Uni"
            },
            "roletype": {
                "id": "ced46aa4-3217-4fc1-b79d-f6be7d21c6b6",
                "name": "administrátor"
            }
        },
        {
            "valid": True,
            "group": {
                "id": "2d9dcd22-a4a2-11ed-b9df-0242ac120003",
                "name": "Uni"
            },
            "roletype": {
                "id": "ae3f0d74-6159-11ed-b753-0242ac120003",
                "name": "rektor"
            }
        }
    ]
}

def getUserFromInfo(info):
    context = info.context
    #print(list(context.keys()))
    user = context.get("user", None)
    if user is None:
        request = context.get("request", None)
        assert request is not None, "request is missing in context :("
        user = request.scope.get("user", None)
        assert user is not None, "missing user in context or in request.scope"
    logging.debug("getUserFromInfo", user)
    return user

def getAuthorizationToken(info):
    context = info.context
    request = context.get("request", None)
    assert request is not None, "trying to get authtoken from None request"

def createLoadersContext(asyncSessionMaker):
    return {
        "loaders": createLoaders(asyncSessionMaker)
    }

def createUgConnectionContext(request):
    from .gql_ug_proxy import get_ug_connection
    connection = get_ug_connection(request=request)
    return {
        "ug_connection": connection
    }

def getUgConnection(info):
    context = info.context
    print("getUgConnection.context", context)
    connection = context.get("ug_connection", None)
    return connection

# def createIdLoader(asyncSessionMaker, dbModel) :

#     mainstmt = select(dbModel)
#     filtermethod = dbModel.id.in_
#     class Loader(DataLoader):
#         async def batch_load_fn(self, keys):
#             #print('batch_load_fn', keys, flush=True)
#             async with asyncSessionMaker() as session:
#                 statement = mainstmt.filter(filtermethod(keys))
#                 rows = await session.execute(statement)
#                 rows = rows.scalars()
#                 #return rows
#                 datamap = {}
#                 for row in rows:
#                     datamap[row.id] = row
#                 result = [datamap.get(id, None) for id in keys]
#                 return result

#         async def insert(self, entity, extraAttributes={}):
#             newdbrow = dbModel()
#             newdbrow = update(newdbrow, entity, extraAttributes)
#             async with asyncSessionMaker() as session:
#                 session.add(newdbrow)
#                 await session.commit()
#             return newdbrow

#         async def update(self, entity, extraValues={}):
#             async with asyncSessionMaker() as session:
#                 statement = mainstmt.filter_by(id=entity.id)
#                 rows = await session.execute(statement)
#                 rows = rows.scalars()
#                 rowToUpdate = next(rows, None)

#                 if rowToUpdate is None:
#                     return None

#                 dochecks = hasattr(rowToUpdate, 'lastchange')             
#                 checkpassed = True  
#                 if (dochecks):
#                     if (entity.lastchange != rowToUpdate.lastchange):
#                         result = None
#                         checkpassed = False                        
#                     else:
#                         entity.lastchange = datetime.datetime.now()
#                 if checkpassed:
#                     rowToUpdate = update(rowToUpdate, entity, extraValues=extraValues)
#                     await session.commit()
#                     result = rowToUpdate
#                     self.registerResult(result)               
#             return result

#         async def delete(self, id):
#             statement = delete(dbModel).where(dbModel.id==id)
#             async with asyncSessionMaker() as session:
#                 result = await session.execute(statement)
#                 await session.commit()
#                 self.clear(id)
#                 return result

#         def registerResult(self, result):
#             self.clear(result.id)
#             self.prime(result.id, result)
#             return result

#         def getSelectStatement(self):
#             return select(dbModel)
        
#         def getModel(self):
#             return dbModel
        
#         def getAsyncSessionMaker(self):
#             return asyncSessionMaker
        
#         async def execute_select(self, statement):
#             async with asyncSessionMaker() as session:
#                 rows = await session.execute(statement)
#                 return (
#                     self.registerResult(row)
#                     for row in rows.scalars()
#                 )
            
#         async def filter_by(self, **filters):
#             statement = mainstmt.filter_by(**filters)
#             return await self.execute_select(statement)

#         async def page(self, skip=0, limit=10, where=None, extendedfilter=None):
#             statement = mainstmt
#             if where is not None:
#                 statement = prepareSelect(dbModel, where)
#             statement = statement.offset(skip).limit(limit)
#             if extendedfilter is not None:
#                 statement = statement.filter_by(**extendedfilter)
#             logging.info(f"loader.page statement {statement}")
#             return await self.execute_select(statement)
            
#         def set_cache(self, cache_object):
#             self.cache = True
#             self._cache = cache_object

#     return Loader(cache=True)
