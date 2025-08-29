from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, UniqueConstraint
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship
from app.database import Base

class Teacher(Base):
    __tablename__ = "teachers"

    teacher_id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.school_id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    teacher_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    # relationships
    school = relationship("School", back_populates="teachers", passive_deletes=True)
    teacher_class_subjects = relationship("TeacherClassSubject", back_populates="teacher", cascade="all, delete")


class TeacherClassSubject(Base):
    __tablename__ = "teacher_class_subjects"

    teacher_class_subjects = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.school_id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.teacher_id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    class_section_id = Column(Integer, ForeignKey("class_sections.class_section_id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.subject_id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)

    teacher = relationship("Teacher", back_populates="teacher_class_subjects")
    class_section = relationship("ClassSection", back_populates="teacher_class_subjects")
    subject = relationship("Subject", back_populates="teacher_class_subjects")

    __table_args__ = (
        UniqueConstraint('school_id', 'teacher_id', 'class_section_id', 'subject_id', name='unique_teacher_class_subject'),
    )
