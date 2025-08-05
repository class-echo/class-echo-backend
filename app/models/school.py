from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import text
from app.database import Base

class School(Base):
    __tablename__ = "schools"

    school_id = Column(Integer, primary_key=True, index=True)
    school_name = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=text('now()'))