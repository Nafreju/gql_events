from sqlalchemy import Column, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now

from .uuid import UUIDColumn, UUIDFKey
from .base import BaseModel

class EventTypeModel(BaseModel):
    __tablename__ = "eventtypes"

    #Atributes
    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)
    category_id = Column(ForeignKey("eventcategories.id"), index=True, nullable=True)
    created = Column(DateTime, server_default=now())
    lastchange = Column(DateTime, server_default=now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

    #sqlalchemy requirements
    events = relationship("EventModel", back_populates="eventtype", uselist=True)
    category = relationship("EventCategoryModel", back_populates="types", uselist=False)