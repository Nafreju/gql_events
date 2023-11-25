import strawberry
import datetime
from typing import Union, List, Annotated, Optional
from .utils import withInfo, getLoaders
from ..GraphResolvers import resolveGroupsForEvent, resolvePresencesForEvent




@strawberry.federation.type(keys=["id"], description="""Entity representing an state exam""")
class StateExamGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: strawberry.ID):
        state_exam_loader = getLoaders(info).stateexams
        result = await state_exam_loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  
        return result

    @strawberry.field(description="""Primary key""")
    def id(self) -> strawberry.ID:
        return self.id

    @strawberry.field(description="""Time stamp""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberry.field(description="""Event name""")
    def name(self) -> Union[str, None]:
        return self.name

    @strawberry.field(description="""Date&time of event begin""")
    def startdate(self) -> Union[datetime.datetime, None]:
        return self.startdate

    @strawberry.field(description="""Date&time of event end""")
    def enddate(self) -> Union[datetime.datetime, None]:
        return self.enddate