from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text
from app.database import Base

class Parent(Base):
    __tablename__ = "parents"

    parent_id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.school_id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    address = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    school = relationship("School", passive_deletes=True)

class StudentParent(Base):
    __tablename__ = "student_parent"

    student_parent_id = Column(Integer, primary_key=True, index=True)
    reg_no = Column(Integer, ForeignKey("students.reg_no", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    parent_id = Column(Integer, ForeignKey("parents.parent_id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    relationship = Column(String)
