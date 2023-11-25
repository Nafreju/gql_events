
from sqlalchemy import Column, Uuid
from uuid import uuid4

def newUuidAsString():
    return f"{uuid4()}"

def UUIDColumn():
    return Column(Uuid, primary_key=True, comment="primary key", default=uuid4)

def UUIDFKey(comment=None, nullable=True, **kwargs):
    return Column(Uuid, index=True, comment=comment, nullable=nullable, **kwargs)