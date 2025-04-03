from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from db import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True,index=True)
    full_name = Column(String(255), nullable=False, unique=False, index=False)
    cert_type = Column(String(255), nullable=False, unique=False, index=False)
    student_id = Column(Integer, nullable=False)
    def __repr__(self):
        return 'TaskModel(full_name=%s, cert_type=%s, student_id=%s)' % (self.full_name, self.cert_type, self.student_id)
    
