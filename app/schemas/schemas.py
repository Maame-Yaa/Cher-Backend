from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime, date


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: str
    last_name: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    username: str
    password: str
    email: EmailStr
    first_name: str
    last_name: str
    created_at: datetime

    model_config = {"from_attributes": True}


class LeadCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    status: str = "new"           
    source: str = "website"       
    budget_min: Optional[int] = None
    budget_max: Optional[int] = None
    property_interest: Optional[str] = None

class Lead(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    status: str
    source: str
    budget_min: Optional[int] = None
    budget_max: Optional[int] = None
    property_interest: Optional[str] = None
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
    activity_count: int = 0

    model_config = {"from_attributes": True}
    

class LeadUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    status: Optional[str] = None
    source: Optional[str] = None
    budget_min: Optional[int] = None
    budget_max: Optional[int] = None
    property_interest: Optional[str] = None


class ActivityCreate(BaseModel):
    lead_id: int
    activity_type: str
    title: str
    notes: Optional[str] = None
    duration: Optional[int] = None
    activity_date: date

class Activity(BaseModel):
    id: int
    lead_id: int
    user_id: int
    activity_type: str
    title: str
    notes: Optional[str] = None
    duration: Optional[int] = None
    activity_date: date
    created_at: datetime
    # user_name: str

    model_config = {"from_attributes": True}


class DashboardStats(BaseModel):
    total_leads: int
    new_leads_this_week: int
    closed_leads_this_month: int
    total_activities: int
    leads_by_status: List[Dict[str, Any]]
    recent_activities: List[Activity]  


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    

class ActivityUpdate(BaseModel):
    lead_id: Optional[int] = None
    activity_type: Optional[str] = None
    title: Optional[str] = None
    notes: Optional[str] = None
    duration: Optional[int] = None
    activity_date: Optional[date] = None