from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import text
from app.database import Base

class Parent(Base):
    __tablename__ = "parents"

    parent_id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.school_id"))
    first_name = Column(String)
    last_name = Column(String)
    phone = Column(String)
    email = Column(String)
    address = Column(String)
    created_at = Column(DateTime, nullable=False, server_default=text('now()'))

class StudentParent(Base):
    __tablename__ = "student_parent"

    student_parent_id = Column(Integer, primary_key=True, index=True)
    reg_no = Column(Integer, ForeignKey("students.reg_no"))
    parent_id = Column(Integer, ForeignKey("parents.parent_id"))
    relationship = Column(String)
