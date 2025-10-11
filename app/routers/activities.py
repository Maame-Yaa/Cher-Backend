from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime, time
from app.core.database import get_db
from app.models.models import Activity as ActivityModel, Lead as LeadModel
from app.schemas.schemas import ActivityCreate, ActivityUpdate, Activity
from app.deps.auth import get_current_user

router = APIRouter(prefix="/activities", tags=["activities"])

@router.post("", response_model=Activity, status_code=status.HTTP_201_CREATED)
def create_activity(
    body: ActivityCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    lead = db.get(LeadModel, body.lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    activity_dt = datetime.combine(body.activity_date, time.min)

    act = ActivityModel(
        lead_id=body.lead_id,
        user_id=current_user.id,
        activity_type=body.activity_type,
        title=body.title,
        notes=body.notes,
        duration=body.duration,
        activity_date=activity_dt,
    )
    db.add(act)

    lead.activity_count = (lead.activity_count or 0) + 1

    db.commit()
    db.refresh(act)
    return act

@router.get("", response_model=list[Activity])
def list_activities(
    lead_id: int | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    q = db.query(ActivityModel).order_by(ActivityModel.activity_date.desc(), ActivityModel.created_at.desc())
    if lead_id is not None:
        q = q.filter(ActivityModel.lead_id == lead_id)
    return q.offset(skip).limit(limit).all()


@router.get("/{activity_id}", response_model=Activity)
def get_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    act = db.get(ActivityModel, activity_id)
    if not act:
        raise HTTPException(status_code=404, detail="Activity not found")
    return act


@router.patch("/{activity_id}", response_model=Activity)
def update_activity(
    activity_id: int,
    body: ActivityUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    act = db.get(ActivityModel, activity_id)
    if not act:
        raise HTTPException(status_code=404, detail="Activity not found")

    updates = body.model_dump(exclude_unset=True)
    if "activity_date" in updates and updates["activity_date"] is not None:
        updates["activity_date"] = datetime.combine(updates["activity_date"], time.min)

    for k, v in updates.items():
        setattr(act, k, v)

    db.commit()
    db.refresh(act)
    return act

@router.delete("/{activity_id}")
def delete_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    act = db.get(ActivityModel, activity_id)
    if not act:
        raise HTTPException(status_code=404, detail="Activity not found")

    lead = db.get(LeadModel, act.lead_id)
    if lead and (lead.activity_count or 0) > 0:
        lead.activity_count = lead.activity_count - 1

    db.delete(act)
    db.commit()
    return {"detail": "Activity deleted"}
