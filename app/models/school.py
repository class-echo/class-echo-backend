from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text
from app.database import Base

class School(Base):
    __tablename__ = "schools"

    school_id = Column(Integer, primary_key=True, index=True)
    school_name = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    address = Column(String)

    users = relationship("User", back_populates="school", passive_deletes=True)
