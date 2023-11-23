import strawberry as strawberryA
import datetime
from typing import Union, List, Annotated, Optional
from .utils import withInfo, getLoaders
from ..GraphResolvers import resolveGroupsForEvent, resolvePresencesForEvent




@strawberryA.federation.type(keys=["id"], description="""Entity representing an state exam""")
class StateExamGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        state_exam_loader = getLoaders(info).stateexams
        result = await state_exam_loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  
        return result

    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Time stamp""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""Event name""")
    def name(self) -> Union[str, None]:
        return self.name

    @strawberryA.field(description="""Date&time of event begin""")
    def startdate(self) -> Union[datetime.datetime, None]:
        return self.startdate

    @strawberryA.field(description="""Date&time of event end""")
    def enddate(self) -> Union[datetime.datetime, None]:
        return self.enddate