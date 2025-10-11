from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.deps.auth import get_current_user
from app.models.models import Lead as LeadModel, Activity as ActivityModel
from app.schemas.schemas import DashboardStats, Activity

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("", response_model=DashboardStats)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    now = datetime.now(timezone.utc)
    week_start = (now - timedelta(days=now.weekday())).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    month_start = datetime(now.year, now.month, 1, tzinfo=timezone.utc)
    if now.month == 12:
        next_month_start = datetime(now.year + 1, 1, 1, tzinfo=timezone.utc)
    else:
        next_month_start = datetime(now.year, now.month + 1, 1, tzinfo=timezone.utc)

    total_leads = db.query(func.count(LeadModel.id)).scalar() or 0
    total_activities = db.query(func.count(ActivityModel.id)).scalar() or 0

    new_leads_this_week = (
        db.query(func.count(LeadModel.id))
        .filter(LeadModel.created_at >= week_start)
        .scalar()
        or 0
    )

    closed_leads_this_month = (
        db.query(func.count(LeadModel.id))
        .filter(
            LeadModel.status == "closed",
            LeadModel.created_at >= month_start,
            LeadModel.created_at < next_month_start,
        )
        .scalar()
        or 0
    )

    rows = (
        db.query(LeadModel.status, func.count(LeadModel.id))
        .group_by(LeadModel.status)
        .all()
    )
    leads_by_status: List[Dict[str, Any]] = [
        {"status": status or "unknown", "count": count or 0} for status, count in rows
    ]

    recent_acts = (
        db.query(ActivityModel)
        .order_by(ActivityModel.created_at.desc())
        .limit(10)
        .all()
    )

    return DashboardStats(
        total_leads=total_leads,
        new_leads_this_week=new_leads_this_week,
        closed_leads_this_month=closed_leads_this_month,
        total_activities=total_activities,
        leads_by_status=leads_by_status,
        recent_activities=recent_acts, 
    )
