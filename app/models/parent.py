from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base

class Parent(Base):
    __tablename__ = "parents"

    parent_id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.school_id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    address = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    # relationships
    school = relationship("School", back_populates="parents", passive_deletes=True)
    students = relationship("StudentParent", back_populates="parent", cascade="all, delete")


class StudentParent(Base):
    __tablename__ = "student_parent"

    student_parent_id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.school_id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    reg_no = Column(Integer, ForeignKey("students.reg_no", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    parent_id = Column(Integer, ForeignKey("parents.parent_id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    relation = Column(String)

    # relationships
    student = relationship("Student", back_populates="parents")
    parent = relationship("Parent", back_populates="students")
