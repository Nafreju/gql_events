from sqlalchemy import Column, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now

from .uuid import UUIDColumn, UUIDFKey
from .base import BaseModel

class EventGroupModel(BaseModel):
    __tablename__ = "events_groups"
    id = UUIDColumn()
    event_id = Column(ForeignKey("events.id"), index=True)
    group_id = UUIDFKey()#Column(ForeignKey("groups.id"), index=True)
                #Column(ForeignKey("groups.id"), index=True)
                #UUIDFKey()

    created = Column(DateTime, server_default=now())
    lastchange = Column(DateTime, server_default=now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

    #event = relationship("EventModel")
    #group = relationship("GroupModel")
