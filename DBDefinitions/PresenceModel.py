from sqlalchemy import Column, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now

from .uuid import UUIDColumn, UUIDFKey
from .base import BaseModel

class PresenceModel(BaseModel):
    __tablename__ = "events_users"
    id = UUIDColumn()

    event_id = Column(ForeignKey("events.id"), index=True)
    user_id = UUIDFKey()#Column(ForeignKey("users.id"), index=True)
    
    invitation_id = Column(ForeignKey("eventinvitationtypes.id"), index=True)
    presencetype_id = Column(ForeignKey("eventpresencetypes.id"), index=True, nullable=True)

    created = Column(DateTime, server_default=now())
    lastchange = Column(DateTime, server_default=now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
