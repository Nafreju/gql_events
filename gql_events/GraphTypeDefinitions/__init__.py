import strawberry as strawberryA

from .utils import withInfo, getLoaders
from .EventGQLModel import EventGQLModel
from .PresenceGQLModel import PresenceGQLModel
from .EventTypeGQLModel import EventTypeGQLModel
from .PresenceTypeGQLModel import PresenceTypeGQLModel
from .InvitationTypeGQLModel import InvitationTypeGQLModel
from .StateExamGQLModel import StateExamGQLModel
from .externals import UserGQLModel, GroupGQLModel










class Query:
    pass



class Mutation:
    pass






















schema = strawberryA.federation.Schema(Query, types=(UserGQLModel,), mutation=Mutation)