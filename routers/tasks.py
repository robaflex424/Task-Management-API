from database.database import LocalSession
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session 
from models.models import Task
from schemas.task import TaskCreate, TaskResponse, TaskUpdate

router = APIRouter(
  prefix="/tasks",
  tags=["tasks"]
)

def get_db():
  db = LocalSession()
  try:
    yield db
  finally: 
    db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# Get all tasks
@router.get("")
async def get_all_tasks(db: db_dependency):
  return db.query(Task).all()


# Create a task
@router.post("", response_model=TaskResponse)
async def create_task(db: db_dependency, task_create: TaskCreate):
  task_model = Task(**task_create.model_dump())
  db.add(task_model)
  db.commit()
  db.refresh(task_model)

  return task_model


# Get specific task by its Id
@router.get("/{task_id}", response_model=TaskResponse)
async def get_task_by_id(db: db_dependency, task_id: int = Path(gt=0)):
  task_model = db.query(Task).filter(Task.id == int(task_id)).first()

  if task_model is None:
    raise HTTPException(
      status_code=404,
      detail="Task not found!"
    )
  
  return task_model


# Update specific task by its Id
@router.put("/{task_id}", response_model=TaskResponse)
async def update_task_by_id(db: db_dependency, task_update: TaskUpdate ,task_id: int = Path(gt=0)):
  task_to_update = db.query(Task).filter(Task.id == int(task_id)).first()

  if task_to_update is None:
    raise HTTPException(
      status_code=404,
      detail='Task not found!'
    )
  
  task_to_update.title = task_update.title
  task_to_update.description = task_update.description
  task_to_update.priority = task_update.priority
  task_to_update.completed = task_update.completed
  task_to_update.due_date = task_update.due_date
  
  db.commit()
  db.refresh(task_to_update)

  return task_to_update


# Delete task by Id
@router.delete("/{task_id}")
async def delete_task_by_id(db: db_dependency, task_id: int = Path(gt=0)):
  task_to_delete = db.query(Task).filter(Task.id == int(task_id)).first()

  if task_to_delete is None:
    raise HTTPException(
      status_code=404,
      detail="Task not found."
    )
  
  db.delete(task_to_delete)
  db.commit()