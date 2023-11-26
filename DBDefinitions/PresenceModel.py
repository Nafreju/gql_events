from sqlalchemy import Column, DateTime, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now

from .uuid import UUIDColumn, UUIDFKey
from .base import BaseModel

class PresenceModel(BaseModel):
    __tablename__ = "events_users"

    id = UUIDColumn()

    event_id = Column(ForeignKey("events.id"), index=True, comment="event which is assigned to user")
    user_id = UUIDFKey(comment="user which is assigned to event")#Column(ForeignKey("users.id"), index=True, comment="user which is assigned to event")
    
    invitation_id = Column(ForeignKey("eventinvitationtypes.id"), index=True, comment="invitation assigned to event/user")
    presencetype_id = Column(ForeignKey("eventpresencetypes.id"), index=True, nullable=True, comment="type of presence assigned to user/event")

    valid = Column(Boolean, default=True, comment="if this entity is valid or invalid")
    created = Column(DateTime, server_default=now(), comment="when this entity has been created")
    lastchange = Column(DateTime, server_default=now(), comment="timestamp / token")
    createdby = UUIDFKey(nullable=True, comment="who has created the entity")
                #Column(ForeignKey("users.id"), index=True, nullable=True, comment="who has created the entity")
    changedby = UUIDFKey(nullable=True, comment="who has changed this entity")
                #Column(ForeignKey("users.id"), index=True, nullable=True, comment="who has changed this entity")

    rbacobject = UUIDFKey(nullable=True, comment="user or group id, determines access")
    
    #sql alchemy requirements
    event = relationship("EventModel", back_populates="presences", uselist=False)
    invitation = relationship("InvitationTypeModel", back_populates="presences", uselist=False)
    presencetype = relationship("PresenceTypeModel", back_populates="presences", uselist=False)