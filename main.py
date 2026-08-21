from typing import Annotated
from fastapi import FastAPI
from sqlalchemy.orm import Session
from database.database import LocalSession
from routers import auth

app = FastAPI()
app.include_router(auth.router)

def get_db():
    db = LocalSession()
    try:
        yield db 
    finally: 
        db.close()


db_dependency = Annotated[Session, get_db]

@app.get('/')
async def get_root():
    return "It works!"