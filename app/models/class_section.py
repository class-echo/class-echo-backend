from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Class(Base):
    __tablename__ = "classes"

    class_id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.school_id", ondelete="RESTRICT", onupdate="CASCADE"), nullable= False)
    class_name = Column(String, nullable= False)

class Section(Base):
    __tablename__ = "sections"

    section_id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.school_id", ondelete="RESTRICT", onupdate="CASCADE"), nullable= False)
    section_name = Column(String, nullable=False)

class ClassSection(Base):
    __tablename__ = "class_sections"

    class_section_id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.school_id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.class_id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    section_id = Column(Integer, ForeignKey("sections.section_id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
