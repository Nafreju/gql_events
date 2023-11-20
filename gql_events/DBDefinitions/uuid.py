
from sqlalchemy import Column, Uuid
from uuid import uuid4

def newUuidAsString():
    return f"{uuid4()}"

def UUIDColumn(name=None):
    if name is None:
        return Column(Uuid, primary_key=True, unique=True, default=newUuidAsString)
    else:
        return Column(
            name, Uuid, primary_key=True, unique=True, default=newUuidAsString
        )   

def UUIDFKey(*, ForeignKey=None, nullable=False):
    if ForeignKey is None:
        return Column(
            Uuid, index=True, nullable=nullable
        )
    else:
        return Column(
            ForeignKey, index=True, nullable=nullable
        )