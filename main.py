from typing import Annotated
from fastapi import FastAPI
from sqlalchemy.orm import Session
from database.database import LocalSession, Base, engine
from routers import auth, tasks

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)
app.include_router(tasks.router)

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