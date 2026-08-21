from typing import Annotated
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserLogin, UserResponse, TokenResponse
from database.database import LocalSession
from fastapi import APIRouter, Depends, HTTPException
from models.models import User
from core.security import hash_password, verify_password, create_access_token


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

def get_db():
    db = LocalSession()
    try: 
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/register", response_model=UserResponse)
async def create_user(db: db_dependency, user_create: UserCreate):
    if db.query(User).filter(
        User.email == user_create.email, 
        User.username == user_create.username).first():
      
      raise HTTPException(
        status_code=404, 
        detail="User with this email or username already exists"
        )
    
    user_model = User(username = user_create.username,
                      email = user_create.email,
                      hashed_password = hash_password(user_create.password)
    )
    
    db.add(user_model)
    db.commit()
    db.refresh(user_model)

    return user_model

@router.post("/login", response_model=TokenResponse)
async def login_user(db: db_dependency, user_login: UserLogin):
  queried_user = db.query(User).filter(User.username == user_login.username).first()
  
  if queried_user is None :
    raise HTTPException(status_code=401, detail="Incorrect credentials.")
  
  if verify_password(user_login.password, queried_user.hashed_password) is False:
    raise HTTPException(status_code=401, detail="Incorrect credentials.")

  access_token = create_access_token(queried_user.id)

  return {
    "access_token": access_token,
    "token_type": "bearer"
  }