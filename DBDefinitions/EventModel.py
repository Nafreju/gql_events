from sqlalchemy import Column, DateTime, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now

from .uuid import UUIDColumn, UUIDFKey
from .base import BaseModel

class EventModel(BaseModel):
    __tablename__ = "events"

    #Atributes
    id = UUIDColumn()
    name = Column(String, comment="name of event")
    name_en = Column(String, comment="name of event in English")

    valid = Column(Boolean, default=True)
    created = Column(DateTime, server_default=now(), comment="when this entity has been created")
    lastchange = Column(DateTime, server_default=now(), comment="timestamp / token")
    createdby = UUIDFKey(nullable=True, comment="who has created the entity")#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True, comment="who has changed this entity")#Column(ForeignKey("users.id"), index=True, nullable=True)
    
    startdate = Column(DateTime, comment="start date of event")
    enddate = Column(DateTime, comment="end date of event")
    
    masterevent_id = Column(ForeignKey("events.id"), index=True, nullable=True)
    eventtype_id = Column(ForeignKey("eventtypes.id"), index=True, nullable=True)

    rbacobject = UUIDFKey(nullable=True, comment="user or group id, determines access")

    #sqlalchemy requirements
    eventtype = relationship("EventTypeModel", back_populates="events", uselist=False)