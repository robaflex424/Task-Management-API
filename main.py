from typing import Annotated
from fastapi import FastAPI
from sqlalchemy.orm import Session
from database.database import LocalSession

app = FastAPI()

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