from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class Subject(Base):
    __tablename__ = "subjects"

    subject_id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.school_id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    subject_name = Column(String, nullable=False)

    subject_classes = relationship("SubjectClass", back_populates="subject", cascade="all, delete")
    teacher_class_subjects = relationship("TeacherClassSubject", back_populates="subject", cascade="all, delete")

    __table_args__ = (
        UniqueConstraint('school_id', 'subject_name', name='unique_school_subject'),
    )


class SubjectClass(Base):
    __tablename__ = "subject_class"

    subject_class_id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.school_id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.subject_id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    class_section_id = Column(Integer, ForeignKey("class_sections.class_section_id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)

    subject = relationship("Subject", back_populates="subject_classes")
    class_section = relationship("ClassSection", back_populates="subject_classes")

    __table_args__ = (
        UniqueConstraint('school_id', 'subject_id', 'class_section_id', name='unique_school_subject_class'),
    )
