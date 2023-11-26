from sqlalchemy import Column, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now

from .uuid import UUIDColumn, UUIDFKey
from .base import BaseModel

class PresenceTypeModel(BaseModel):
    __tablename__ = "eventpresencetypes"
    id = UUIDColumn()

    name = Column(String)
    name_en = Column(String)
    # present, vacantion, ...

    created = Column(DateTime, server_default=now())
    lastchange = Column(DateTime, server_default=now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

    rbacobject = UUIDFKey(nullable=True, comment="user or group id, determines access")

    #sqlalchemy requirements
    presences = relationship("PresenceModel", back_populates="presencetype", uselist=True)