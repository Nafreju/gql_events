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

    valid = Column(Boolean, default=True, comment="if this entity is valid or invalid")
    created = Column(DateTime, server_default=now(), comment="when this entity has been created")
    lastchange = Column(DateTime, server_default=now(), comment="timestamp / token")
    createdby = UUIDFKey(nullable=True, comment="who has created the entity")
                #Column(ForeignKey("users.id"), index=True, nullable=True, comment="who has created the entity")
    changedby = UUIDFKey(nullable=True, comment="who has changed this entity")
                #Column(ForeignKey("users.id"), index=True, nullable=True, comment="who has changed this entity")
    
    startdate = Column(DateTime, comment="start date of event")
    enddate = Column(DateTime, comment="end date of event")
    
    masterevent_id = Column(ForeignKey("events.id"), index=True, nullable=True, comment="master event which other events are part of including this")
    eventtype_id = Column(ForeignKey("eventtypes.id"), index=True, comment="event type of this event")

    rbacobject = UUIDFKey(nullable=True, comment="user or group id, determines access")

    #sqlalchemy requirements
    eventtype = relationship("EventTypeModel", back_populates="events", uselist=False)
    presences = relationship("PresenceModel", back_populates="event", uselist=True)


    """
    #https://docs.sqlalchemy.org/en/20/orm/inheritance.html#joined-table-inheritance
    __mapper_args__ = {
        "polymorphic_identity": "event",
        "polymorphic_on": "type",
    }
    """