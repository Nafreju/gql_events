from sqlalchemy import Column, DateTime, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now

from .uuid import UUIDColumn, UUIDFKey
from .base import BaseModel

#solves problem with many to many relationship between event and group
class EventGroupModel(BaseModel):
    
    __tablename__ = "events_groups"
    id = UUIDColumn()
    event_id = Column(ForeignKey("events.id"), index=True, comment="event which is assigned to group")
    group_id = UUIDFKey(comment="group which is assigned to event")
                #Column(ForeignKey("groups.id"), index=True, comment="group which is assigned to event")

    valid = Column(Boolean, default=True, comment="if this entity is valid or invalid")
    created = Column(DateTime, server_default=now(), comment="when this entity has been created")
    lastchange = Column(DateTime, server_default=now(), comment="timestamp / token")
    createdby = UUIDFKey(nullable=True, comment="who has created the entity")
                #Column(ForeignKey("users.id"), index=True, nullable=True, comment="who has created the entity")
    changedby = UUIDFKey(nullable=True, comment="who has changed this entity")
                #Column(ForeignKey("users.id"), index=True, nullable=True, comment="who has changed this entity")

    rbacobject = UUIDFKey(nullable=True, comment="user or group id, determines access")

    #sqlalchemy requirements
    event = relationship("EventModel")
    #group = relationship("GroupModel")
