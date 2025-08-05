from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Class(Base):
    __tablename__ = "classes"

    class_id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.school_id"))
    class_name = Column(String)

class Section(Base):
    __tablename__ = "sections"

    section_id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.school_id"))
    section_name = Column(String)

class ClassSection(Base):
    __tablename__ = "class_sections"

    class_section_id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.school_id"))
    class_id = Column(Integer, ForeignKey("classes.class_id"))
    section_id = Column(Integer, ForeignKey("sections.section_id"))
