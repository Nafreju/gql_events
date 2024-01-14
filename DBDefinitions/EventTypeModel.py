from sqlalchemy import Column, DateTime, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now

from .uuid import UUIDColumn, UUIDFKey
from .base import BaseModel

class EventTypeModel(BaseModel):
    __tablename__ = "eventtypes"

    #Atributes
    id = UUIDColumn()
    name = Column(String, comment="name of type")
    name_en = Column(String, comment="name of type in English")

    valid = Column(Boolean, default=True, comment="if this entity is valid or invalid")
    created = Column(DateTime, server_default=now(), comment="when this entity has been created")
    lastchange = Column(DateTime, server_default=now(), comment="timestamp / token")
    createdby = UUIDFKey(nullable=True, comment="who has created the entity")
                #Column(ForeignKey("users.id"), index=True, nullable=True, comment="who has created the entity")
    changedby = UUIDFKey(nullable=True, comment="who has changed this entity")
                #Column(ForeignKey("users.id"), index=True, nullable=True, comment="who has changed this entity")

    category_id = Column(ForeignKey("eventcategories.id"), index=True, nullable=True, comment="category of this event type")

    rbacobject = UUIDFKey(nullable=True, comment="user or group id, determines access")

    #sqlalchemy requirements
    events = relationship("EventModel", back_populates="eventtype", uselist=True)
    category = relationship("EventCategoryModel", back_populates="eventtypes", uselist=False)