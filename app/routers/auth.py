from fastapi import APIRouter, Depends, HTTPException, status        
from sqlalchemy.orm import Session                                   
from app.core.database import get_db                                  
from app.models.models import User as UserModel                   
from app.schemas.schemas import UserCreate, UserLogin, Token, User
from app.deps.auth import hash_password, verify_password, create_access_token, get_current_user
from fastapi.security import OAuth2PasswordRequestForm 
                       

router = APIRouter(prefix="/auth", tags=["auth"]) 

@router.post("/register", response_model=User)                                        
def register(body: UserCreate, db: Session = Depends(get_db)):     
    exists = db.query(UserModel).filter(UserModel.username == body.username).first() 
    if exists:                                                       
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,  
                            detail="Username already taken")
    
    existing_email = db.query(UserModel).filter(UserModel.email == body.email).first()
    if existing_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    hashed_pw = hash_password(body.password)
    new_user = UserModel(
        username=body.username,
        email=body.email,
        hashed_password=hashed_pw,
        first_name=body.first_name,
        last_name=body.last_name
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post('/login', response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    token = create_access_token({"sub": str(user.id)})
    return {'access_token': token, "token_type":'bearer'}


@router.get("/me", response_model=User)
def me(current_user = Depends(get_current_user)):
    return current_user





