from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text # For server default timestamp

class Student(Base):
    __tablename__ = "students"

    reg_no = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.school_id", ondelete="CASCADE"))
    f_name = Column(String, nullable=False)
    l_name = Column(String, nullable=False)
    address = Column(String)
    admit_date = Column(DateTime)
    leave_date = Column(DateTime)
    created_at = Column(DateTime, nullable=False, server_default=text('now()'))

    school = relationship("School", passive_deletes=True)

class StudentClass(Base):
    __tablename__ = "student_class"

    sc_id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.school_id", ondelete="CASCADE"))
    reg_no = Column(Integer, ForeignKey("students.reg_no", ondelete="CASCADE"))
    class_section_id = Column(Integer, ForeignKey("class_sections.class_section_id", ondelete="CASCADE"))
