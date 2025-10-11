from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Lead as LeadModel
from app.schemas.schemas import LeadCreate, Lead, LeadUpdate
from app.deps.auth import get_current_user 

router = APIRouter(prefix="/leads", tags=["leads"])

@router.post("", response_model=Lead, status_code=status.HTTP_201_CREATED)
def create_lead(body: LeadCreate, 
                db: Session = Depends(get_db), 
                current_user = Depends(get_current_user)):

    exists = db.query(LeadModel).filter(LeadModel.email == body.email).first()
    if exists:
        raise HTTPException(status_code=400, detail="Lead with that email already exists")

    lead = LeadModel(
        email=body.email,
        first_name=body.first_name,
        last_name=body.last_name,
        status=body.status,
        phone=body.phone,
        source=body.source,
        budget_min=body.budget_min,
        budget_max=body.budget_max,
        property_interest=body.property_interest,
        is_active=True,
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead

@router.get("", response_model=list[Lead])
def list_leads(skip: int = Query(0, ge=0), 
               limit: int = Query(20, ge=1, le=100),
               db: Session = Depends(get_db),
               current_user = Depends(get_current_user)):
    rows = (db.query(LeadModel)
              .filter(LeadModel.is_active == True)
              .order_by(LeadModel.created_at.desc())
              .offset(skip)
              .limit(limit)
              .all())
    return rows

@router.get("/{lead_id}", response_model=Lead)
def get_lead(lead_id: int,
             db: Session = Depends(get_db),
             current_user = Depends(get_current_user)):
    lead = db.get(LeadModel, lead_id)
    if not lead or not lead.is_active:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


@router.patch("/{lead_id}", response_model=Lead)
def update_lead(lead_id: int,
                body: LeadUpdate,
                db: Session = Depends(get_db),
                current_user = Depends(get_current_user)):
    lead = db.get(LeadModel, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    updates = body.model_dump(exclude_unset=True)
    for k, v in updates.items():
        setattr(lead, k, v)

    db.commit()
    db.refresh(lead)
    return lead



@router.delete("/{lead_id}")
def delete_lead(lead_id: int, 
                db: Session = Depends(get_db),
                current_user = Depends(get_current_user)):
    lead = db.get(LeadModel, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    lead.is_active = False
    db.commit()
    return {"detail": "Lead deactivated"}