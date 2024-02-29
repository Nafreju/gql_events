

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .EventModel import EventModel
from .uuid import UUIDFKey

"""
Events mají svoji tabulku
Exam má svoji tabulku obsahující jen atributy, které jsou navíc --- 


polymorphic_on znamená, že Events budou mít v tabulce sloupec s type a hodnout "events"
zatímco Exams budou mít v type "exams" (dle polymorphic_identity)
"""

#https://docs.sqlalchemy.org/en/20/orm/inheritance.html#joined-table-inheritance
class ExamModel(EventModel):
    __tablename__ = "eventexams"
    #or
    __tablename__ = "exams"

    id = Column(ForeignKey("events.id"), primary_key=True, comment="which event is this exam")
    term = Column(String, default=1, comment="which term is this subject exam") #řádný, první opravný, ...
    #to get which term is for given student(user) use "COUNT of presences, where invitationtype like "zkoušený" 
    # and event.type is "exams" (type as polymorphism)"

    #subject has multiple Exams (different terms)
    subject_id = UUIDFKey(nullable=True, comment="subject of this exam")
            #Column(ForeignKey("acsubjects.id"), index=True, comment="subject of this exam")
    
    #from federation
    #subject = relationship("SubjectModel", back_populates="exams", uselist=False) 
    
    
    
    __mapper_args__ = {
        "polymorphic_identity": "exam",
    }