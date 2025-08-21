from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Enum
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class UserRole(enum.Enum):
    super_admin = "super_admin"
    school_admin = "school_admin"
    teacher = "teacher"
    student = "student"
    parent = "parent"


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=True)  # will be null if using Google login only
    role = Column(Enum(UserRole), nullable=False)
    school_id = Column(Integer, ForeignKey("schools.school_id", ondelete="CASCADE"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # relation to school
    school = relationship("School", back_populates="users", passive_deletes=True)
