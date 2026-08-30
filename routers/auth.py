from typing import Annotated
from sqlalchemy import or_
from sqlalchemy.orm import Session
from schemas.user import (
  UserCreate, 
  UserLogin, 
  UserResponse, 
  TokenResponse
)
from database.database import get_db
from fastapi import (
  APIRouter, 
  Depends, 
  HTTPException)
from models.models import User
from core.security import (
  hash_password, 
  verify_password, 
  create_access_token, 
  decode_access_token
)
from fastapi.security import OAuth2PasswordBearer


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

db_dependency = Annotated[Session, Depends(get_db)]
token_dependency = Annotated[str, Depends(oauth2_scheme)]

def get_current_user(token: token_dependency, db: db_dependency):
  user_id = decode_access_token(token)

  if user_id is None:
    raise HTTPException(
      status_code=401,
      detail="Could not validate credentials."
    )
  
  user = db.query(User).filter(User.id == int(user_id)).first() 

  if user is None:
    raise HTTPException(
      status_code=401, 
      detail="User not found."
    )
  
  return user

current_user_dependency = Annotated[User, Depends(get_current_user)]

@router.get("/me")
async def get_me(current_user: Annotated[User, Depends(get_current_user)]):
  return current_user


@router.post("/register", response_model=UserResponse)
async def create_user(
  db: db_dependency, 
  user_create: UserCreate
  ):

  existing_user = db.query(User).filter(
    or_(
      User.email == user_create.email
    )
  ).first()

  if existing_user:
    raise HTTPException(
      status_code=409,
      detail="Email or username already registered."
    )

  user_model = User(
    username=user_create.username,
    email=user_create.email,
    hashed_password=hash_password(user_create.password)
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
