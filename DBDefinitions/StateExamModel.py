from sqlalchemy import Column, DateTime, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now

from .uuid import UUIDColumn, UUIDFKey
from .base import BaseModel

#use EventGQLModel, EventTypeGQLModel, UserGQLModel, GroupGQLModel

class StateExamModel(BaseModel):
    __tablename__ = "eventstateexams"

    id = UUIDColumn()
    startdate = Column(DateTime)
    enddate = Column(DateTime)
    name = Column(String)
    name_en = Column(String)

    group_id = Column(ForeignKey("group.id"), index=True, comment="group which is assigned to event")
    event_id = Column(ForeignKey("events.id"), index=True, comment="event which is assigned to user")
    user_id = UUIDFKey(comment="user which is assigned to event")#Column(ForeignKey("users.id"), index=True, comment="user which is assigned to event")
    #eventtype_id
    #grouptype_id
    valid = Column(Boolean, default=True, comment="if this entity is valid or invalid")
    created = Column(DateTime, server_default=now(), comment="when this entity has been created")
    lastchange = Column(DateTime, server_default=now(), comment="timestamp / token")
    createdby = UUIDFKey(nullable=True, comment="who has created the entity")
                #Column(ForeignKey("users.id"), index=True, nullable=True, comment="who has created the entity")
    changedby = UUIDFKey(nullable=True, comment="who has changed this entity")
                #Column(ForeignKey("users.id"), index=True, nullable=True, comment="who has changed this entity")

