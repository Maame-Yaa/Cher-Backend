from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    

class Lead(Base):
    __tablename__ = 'leads'
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    status = Column(String)
    phone = Column(String)
    source = Column(String)
    budget_min = Column(Integer, nullable=True)
    budget_max = Column(Integer, nullable=True)
    property_interest = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc))
    activity_count = Column(Integer, default = 0)
    
    
class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)

    activity_type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    notes = Column(String, nullable=True)
    duration = Column(Integer, nullable=True)    
    activity_date = Column(DateTime, nullable=False)

    created_at = Column(DateTime, default=datetime.now(timezone.utc))