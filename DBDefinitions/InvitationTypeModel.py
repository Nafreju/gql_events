from sqlalchemy import Column, DateTime, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now

from .uuid import UUIDColumn, UUIDFKey
from .base import BaseModel


class InvitationTypeModel(BaseModel):
    __tablename__ = "eventinvitationtypes"

    #Atributes
    id = UUIDColumn()
    name = Column(String, comment="name of invitation type to event")
    name_en = Column(String, comment="name of invitation type to event in English")
    # initiator, invited mandatory, invited voluntary, accepted, tentatively accepted, rejected,

    valid = Column(Boolean, default=True, comment="if this entity is valid or invalid")
    created = Column(DateTime, server_default=now(), comment="when this entity has been created")
    lastchange = Column(DateTime, server_default=now(), comment="timestamp / token")
    createdby = UUIDFKey(nullable=True, comment="who has created the entity")
                #Column(ForeignKey("users.id"), index=True, nullable=True, comment="who has created the entity")
    changedby = UUIDFKey(nullable=True, comment="who has changed this entity")
                #Column(ForeignKey("users.id"), index=True, nullable=True, comment="who has changed this entity")
    
    rbacobject = UUIDFKey(nullable=True, comment="user or group id, determines access")
    
    #sqlalchemy requirements
    presences = relationship("PresenceModel", back_populates="invitation", uselist=True)