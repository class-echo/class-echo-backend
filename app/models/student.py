from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, UniqueConstraint
from app.database import Base
from sqlalchemy.orm import relationship

class Student(Base):
    __tablename__ = "students"

    reg_no = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.school_id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    f_name = Column(String, nullable=False)
    l_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    address = Column(String)
    admit_date = Column(DateTime)
    leave_date = Column(DateTime)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    # relationships
    school = relationship("School", back_populates="students", passive_deletes=True)
    student_classes = relationship("StudentClass", back_populates="student", cascade="all, delete")
    parents = relationship("StudentParent", back_populates="student", cascade="all, delete")


class StudentClass(Base):
    __tablename__ = "student_class"

    student_class_id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.school_id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    reg_no = Column(Integer, ForeignKey("students.reg_no", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    class_section_id = Column(Integer, ForeignKey("class_sections.class_section_id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)

    # relationships
    student = relationship("Student", back_populates="student_classes")
    class_section = relationship("ClassSection", back_populates="student_classes")

    __table_args__ = (
        UniqueConstraint('school_id', 'reg_no', 'class_section_id', name='unique_student_class'),
    )
