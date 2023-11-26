import strawberry
import datetime
from typing import Union, List, Annotated, Optional
from .utils import withInfo, getLoaders, getUser
from uuid import UUID


@strawberry.federation.type(keys=["id"], description="""Represents category of event""")
class EventCategoryGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: UUID):
        loader = getLoaders(info).eventcategories
        result = loader.load(id)
        if result is not None:
            result.__strawberry_definition__ = cls.__strawberry_definition__   # little hack :)
        return result
