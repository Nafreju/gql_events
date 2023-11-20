from sqlalchemy import Column, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now

from .uuid import UUIDColumn, UUIDFKey
from .base import BaseModel

class EventModel(BaseModel):
    __tablename__ = "events"

    id = UUIDColumn()
    name = Column(String)
    startdate = Column(DateTime)
    enddate = Column(DateTime)

    created = Column(DateTime, server_default=now())
    lastchange = Column(DateTime, server_default=now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    masterevent_id = Column(ForeignKey("events.id"), index=True, nullable=True)
    eventtype_id = Column(ForeignKey("eventtypes.id"), index=True)
    eventtype = relationship("EventTypeModel", back_populates="events")