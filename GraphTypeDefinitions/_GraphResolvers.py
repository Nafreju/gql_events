import strawberry
import uuid
import datetime
import typing
import logging




from inspect import signature
import inspect 
from functools import wraps

def asPage(field, *, extendedfilter=None):
    def decorator(field):
        print(field.__name__, field.__annotations__)
        signatureField = signature(field)
        return_annotation = signatureField.return_annotation

        skipParameter = signatureField.parameters.get("skip", None)
        skipParameterDefault = 0
        if skipParameter:
            skipParameterDefault = skipParameter.default

        limitParameter = signatureField.parameters.get("limit", None)
        limitParameterDefault = 10
        if limitParameter:
            limitParameterDefault = limitParameter.default

        whereParameter = signatureField.parameters.get("where", None)
        whereParameterDefault = None
        whereParameterAnnotation = str
        if whereParameter:
            whereParameterDefault = whereParameter.default
            whereParameterAnnotation = whereParameter.annotation

        async def foreignkeyVectorSimple(
            self, info: strawberry.types.Info,
            skip: typing.Optional[int] = skipParameterDefault,
            limit: typing.Optional[int] = limitParameterDefault
        ) -> signature(field).return_annotation:
            loader = await field(self, info)
            results = await loader.page(skip=skip, limit=limit, extendedfilter=extendedfilter)
            return results
        foreignkeyVectorSimple.__name__ = field.__name__
        foreignkeyVectorSimple.__doc__ = field.__doc__

        async def foreignkeyVectorComplex(
            self, info: strawberry.types.Info, 
            where: whereParameterAnnotation = None, 
            #where: typing.Optional[whereParameterAnnotation] = whereParameterDefault, 
            #where: typing.Optional[str] = None, 
            orderby: typing.Optional[str] = None, 
            desc: typing.Optional[bool] = None, 
            skip: typing.Optional[int] = skipParameterDefault,
            limit: typing.Optional[int] = limitParameterDefault
        ) -> signatureField.return_annotation:
            # logging.info(f"waiting for a loader {where}")
            wf = None if where is None else strawberry.asdict(where)
            loader = await field(self, info, where=wf)    
            # logging.info(f"got a loader {loader}")
            # wf = None if where is None else strawberry.asdict(where)
            results = await loader.page(skip=skip, limit=limit, where=wf, orderby=orderby, desc=desc, extendedfilter=extendedfilter)
            return results
        foreignkeyVectorComplex.__name__ = field.__name__
        foreignkeyVectorComplex.__doc__ = field.__doc__
        
        if return_annotation._name == "List":
            return foreignkeyVectorComplex if whereParameter else foreignkeyVectorSimple
        else:
            raise Exception("Unable to recognize decorated function, I am sorry")

    return decorator(field) if field else decorator

def asForeignList(*, foreignKeyName: str):
    assert foreignKeyName is not None, "foreignKeyName must be defined"
    def decorator(field):
        print(field.__name__, field.__annotations__)
        signatureField = signature(field)
        return_annotation = signatureField.return_annotation

        skipParameter = signatureField.parameters.get("skip", None)
        skipParameterDefault = skipParameter.default if skipParameter else 0

        limitParameter = signatureField.parameters.get("limit", None)
        limitParameterDefault = limitParameter.default if limitParameter else 10

        whereParameter = signatureField.parameters.get("where", None)
        whereParameterDefault = whereParameter.default if whereParameter else None
        whereParameterAnnotation = whereParameter.annotation if whereParameter else str

        async def foreignkeyVectorSimple(
            self, info: strawberry.types.Info,
            skip: typing.Optional[int] = skipParameterDefault,
            limit: typing.Optional[int] = limitParameterDefault
        ) -> signature(field).return_annotation:
            extendedfilter = {}
            extendedfilter[foreignKeyName] = self.id
            loader = field(self, info)
            if inspect.isawaitable(loader):
                loader = await loader
            results = await loader.page(skip=skip, limit=limit, extendedfilter=extendedfilter)
            return results
        foreignkeyVectorSimple.__name__ = field.__name__
        foreignkeyVectorSimple.__doc__ = field.__doc__
        foreignkeyVectorSimple.__module__ = field.__module__

        async def foreignkeyVectorComplex(
            self, info: strawberry.types.Info, 
            where: whereParameterAnnotation = whereParameterDefault, 
            orderby: typing.Optional[str] = None, 
            desc: typing.Optional[bool] = None, 
            skip: typing.Optional[int] = skipParameterDefault,
            limit: typing.Optional[int] = limitParameterDefault
        ) -> signatureField.return_annotation:
            extendedfilter = {}
            extendedfilter[foreignKeyName] = self.id
            loader = field(self, info)
            if inspect.isawaitable(loader):
                loader = await loader
            
            wf = None if where is None else strawberry.asdict(where)
            results = await loader.page(skip=skip, limit=limit, where=wf, orderby=orderby, desc=desc, extendedfilter=extendedfilter)
            return results
        foreignkeyVectorComplex.__name__ = field.__name__
        foreignkeyVectorComplex.__doc__ = field.__doc__
        foreignkeyVectorComplex.__module__ = field.__module__

        async def foreignkeyVectorComplex2(
            self, info: strawberry.types.Info, 
            where: whereParameterAnnotation = whereParameterDefault, 
            orderby: typing.Optional[str] = None, 
            desc: typing.Optional[bool] = None, 
            skip: typing.Optional[int] = skipParameterDefault,
            limit: typing.Optional[int] = limitParameterDefault
        ) -> signatureField.return_annotation: #typing.List[str]:
            extendedfilter = {}
            extendedfilter[foreignKeyName] = self.id
            loader = field(self, info)
            
            wf = None if where is None else strawberry.asdict(where)
            results = await loader.page(skip=skip, limit=limit, where=wf, orderby=orderby, desc=desc, extendedfilter=extendedfilter)
            return results
        foreignkeyVectorComplex2.__module__ = field.__module__
        if return_annotation._name == "List":
            return foreignkeyVectorComplex if whereParameter else foreignkeyVectorSimple
        else:
            raise Exception("Unable to recognize decorated function, I am sorry")

    return decorator
# def createAttributeScalarResolver(

# def createAttributeScalarResolver(
#     scalarType: None = None, 
#     foreignKeyName: str = None,
#     description="Retrieves item by its id",
#     permission_classes=()
#     ):

#     assert scalarType is not None
#     assert foreignKeyName is not None

#     @strawberry.field(description=description, permission_classes=permission_classes)
#     async def foreignkeyScalar(
#         self, info: strawberry.types.Info
#     ) -> typing.Optional[scalarType]:
#         # 👇 self must have an attribute, otherwise it is fail of definition
#         assert hasattr(self, foreignKeyName)
#         id = getattr(self, foreignKeyName, None)
        
#         result = None if id is None else await scalarType.resolve_reference(info=info, id=id)
#         return result
#     return foreignkeyScalar

# def createAttributeVectorResolver(
#     scalarType: None = None, 
#     whereFilterType: None = None,
#     foreignKeyName: str = None,
#     loaderLambda = lambda info: None, 
#     description="Retrieves items paged", 
#     skip: int=0, 
#     limit: int=10):

#     assert scalarType is not None
#     assert foreignKeyName is not None

#     @strawberry.field(description=description)
#     async def foreignkeyVector(
#         self, info: strawberry.types.Info,
#         skip: int = skip,
#         limit: int = limit,
#         where: typing.Optional[whereFilterType] = None
#     ) -> typing.List[scalarType]:
        
#         params = {foreignKeyName: self.id}
#         loader = loaderLambda(info)
#         assert loader is not None
        
#         wf = None if where is None else strawberry.asdict(where)
#         result = await loader.page(skip=skip, limit=limit, where=wf, extendedfilter=params)
#         return result
#     return foreignkeyVector

from uuid import UUID
def createRootResolver_by_id(scalarType: None, description="Retrieves item by its id"):
    assert scalarType is not None
    @strawberry.field(description=description)
    async def by_id(
        self, info: strawberry.types.Info, id: UUID(id)
    ) -> typing.Optional[scalarType]:
        result = await scalarType.resolve_reference(info=info, id=id)
        return result
    return by_id

def createRootResolver_by_page(
    scalarType: None, 
    whereFilterType: None,
    loaderLambda = lambda info: None, 
    description="Retrieves items paged", 
    skip: int=0, 
    limit: int=10,
    order_by: typing.Optional[str] = None,
    desc: typing.Optional[bool] = None):

    assert scalarType is not None
    assert whereFilterType is not None
    
    @strawberry.field(description=description)
    async def paged(
        self, info: strawberry.types.Info, 
        skip: int=skip, limit: int=limit, where: typing.Optional[whereFilterType] = None
    ) -> typing.List[scalarType]:
        loader = loaderLambda(info)
        assert loader is not None
        wf = None if where is None else strawberry.asdict(where)
        result = await loader.page(skip=skip, limit=limit, where=wf, orderby=order_by, desc=desc)
        return result
    return paged


from sqlalchemy.future import select
from DBDefinitions import EventModel, EventGroupModel, PresenceModel

def create_statement_for_group_events(id, startdate=None, enddate=None):
    statement = select(EventModel).join(EventGroupModel)
    if startdate is not None:
        statement = statement.filter(EventModel.startdate >= startdate)
    if enddate is not None:
        statement = statement.filter(EventModel.enddate <= enddate)
    statement = statement.filter(EventGroupModel.group_id == id)

    return statement

#odstranit?
def create_statement_for_user_events(id, startdate=None, enddate=None):
    statement = select(EventModel).join(PresenceModel)
    if startdate is not None:
        statement = statement.filter(EventModel.startdate >= startdate)
    if enddate is not None:
        statement = statement.filter(EventModel.enddate <= enddate)
    statement = statement.filter(PresenceModel.user_id == id)
    return statement


async def resolvePresencesForEvent(session, id, invitationtypelist=[]):
    statement = select(PresenceModel)
    if len(invitationtypelist) > 0:
        statement = statement.filter(PresenceModel.invitation_id.in_(invitationtypelist))
    response = await session.execute(statement)
    result = response.scalars()
    return result