from uoishelpers.dataloaders import createIdLoader, createFkeyLoader
from functools import cache

from gql_events.DBDefinitions import \
    EventModel, EventTypeModel, EventCategoryModel, EventGroupModel, \
        InvitationTypeModel, PresenceModel, PresenceTypeModel


async def createLoaders(asyncSessionMaker):


    class Loaders:
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