from sqlalchemy import Column, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now

from .uuid import UUIDColumn, UUIDFKey
from .base import BaseModel


class InvitationTypeModel(BaseModel):
    __tablename__ = "eventinvitationtypes"
    id = UUIDColumn()

    name = Column(String)
    name_en = Column(String)
    # initiator, invited mandatory, invited voluntary, accepted, tentatively accepted, rejected,

    created = Column(DateTime, server_default=now())
    lastchange = Column(DateTime, server_default=now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
