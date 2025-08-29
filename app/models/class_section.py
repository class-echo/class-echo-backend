from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Class(Base):
    __tablename__ = "classes"

    class_id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.school_id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    class_name = Column(String, nullable=False)

    # reverse relation to ClassSection
    class_sections = relationship("ClassSection", back_populates="class_", cascade="all, delete")


class Section(Base):
    __tablename__ = "sections"

    section_id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.school_id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    section_name = Column(String, nullable=False)

    # reverse relation to ClassSection
    class_sections = relationship("ClassSection", back_populates="section", cascade="all, delete")


class ClassSection(Base):
    __tablename__ = "class_sections"

    class_section_id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.school_id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.class_id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    section_id = Column(Integer, ForeignKey("sections.section_id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)

    # backrefs
    class_ = relationship("Class", back_populates="class_sections")
    section = relationship("Section", back_populates="class_sections")

    student_classes = relationship("StudentClass", back_populates="class_section", cascade="all, delete")
    teacher_class_subjects = relationship("TeacherClassSubject", back_populates="class_section", cascade="all, delete")
    subject_classes = relationship("SubjectClass", back_populates="class_section", cascade="all, delete")
