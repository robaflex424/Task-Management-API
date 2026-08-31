from database.database import LocalSession
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session 
from models.models import Task
from schemas.task import TaskCreate, TaskResponse, TaskUpdate
from datetime import datetime
from routers.auth import current_user_dependency, get_current_user
from database.database import get_db

router = APIRouter(
  prefix="/tasks",
  tags=["tasks"]
)

db_dependency = Annotated[Session, Depends(get_db)]

# Get all tasks
@router.get("", response_model=list[TaskResponse])
async def get_all_tasks(
  db: db_dependency,
  current_user: current_user_dependency,
  limit: int = Query(default=10, gt=0),
  offset: int = Query(default=0, ge=0)
  ):

  tasks = (
    db.query(Task)
    .filter(Task.user_id == current_user.id)
    .limit(limit)
    .offset(offset)
    .all()
  )

  return tasks


# Create a task
@router.post("", response_model=TaskResponse, status_code=201)
async def create_task(
    db: db_dependency, 
    current_user: current_user_dependency,
    task_create: TaskCreate
  ):
  
  task_model = Task(**task_create.model_dump(), user_id=current_user.id)

  db.add(task_model)
  db.commit()
  db.refresh(task_model)

  return task_model


# Get specific task by its Id
@router.get("/{task_id}", response_model=TaskResponse)
async def get_task_by_id(
    db: db_dependency, 
    current_user: current_user_dependency,
    task_id: int = Path(gt=0)
  ):
  task_model = (
    db.query(Task)
    .filter(
      Task.id == task_id, 
      Task.user_id == current_user.id
    )
    .first()
  )

  if task_model is None:
    raise HTTPException(
      status_code=404,
      detail="Task not found!"
    )
  
  return task_model


# Update specific task by its Id
@router.put("/{task_id}", response_model=TaskResponse)
async def update_task_by_id(
    db: db_dependency, 
    current_user: current_user_dependency,
    task_update: TaskUpdate, 
    task_id: int = Path(gt=0)
  ):

  task_to_update = (
    db.query(Task)
    .filter(
      Task.id == task_id, 
      Task.user_id == current_user.id
    )
    .first()
  )

  if task_to_update is None:
    raise HTTPException(
      status_code=404,
      detail='Task not found!'
    )
  
  update_data = task_update.model_dump(exclude_unset=True)

  for field, value in update_data.items():
    setattr(task_to_update, field, value)
  
  db.commit()
  db.refresh(task_to_update)

  return task_to_update


# Delete task by Id
@router.delete("/{task_id}", status_code=204)
async def delete_task_by_id(
  db: db_dependency,
  current_user: current_user_dependency, 
  task_id: int = Path(gt=0)
  ):

  task_to_delete = (
    db.query(Task)
    .filter(
      Task.id == task_id,
      Task.user_id == current_user.id
      )
      .first()
    )

  if task_to_delete is None:
    raise HTTPException(
      status_code=404,
      detail="Task not found."
    )
  
  db.delete(task_to_delete)
  db.commit()


# Filter tasks based on priority, date of which the task is due, and if completed/uncompleted
@router.get("", response_model=list[TaskResponse])
async def get_filtered_tasks(
    db: db_dependency, 
    current_user: current_user_dependency,
    completed: bool | None = None, 
    priority: int | None = None, 
    due_date: datetime | None = None):
  query = db.query(Task).filter(Task.user_id == current_user.id)

  if completed is not None:
    query = query.filter(Task.completed == completed)
  if priority is not None:
    query = query.filter(Task.priority == priority)
  if due_date is not None:
    query = query.filter(Task.due_date == due_date)
  
  return query.all()


# Sort tasks based on their date of creation, date of which the task is due, and priority
@router.get("", response_model=list[TaskResponse])
async def get_sorted_tasks(
  db: db_dependency,
  current_user: current_user_dependency,
  sort_by: str,
  limit: int = Query(default=10, gt=0),
  offset: int = Query(default=0, ge=0)
):
  query = db.query(Task).filter(Task.user_id == current_user.id)

  if sort_by == "created_at":
    query = query.order_by(Task.created_at.desc())
  
  elif sort_by == "due_date":
    query = query.order_by(Task.due_date.desc())
  
  elif sort_by == "priority":
    query = query.order_by(Task.priority.desc())
  
  else:
    raise HTTPException(
      status_code=400,
      detail="Invalid sort field. Use created_at, due_date, or priority."
    )

  query = query.limit(limit).offset(offset)

  return query.all()


# Search for tasks based on their title and description
@router.get("", response_model=list[TaskResponse])
async def search_tasks(
  db: db_dependency,
  current_user: current_user_dependency,
  query: str,
  limit: int = Query(default=10, gt=0),
  offset: int = Query(default=0, ge=0) 
  ):

    tasks = db.query(Task).filter(
      Task.title.ilike(f"%{query}%") |
      Task.description.ilike(f"%{query}%"),
      Task.user_id == current_user.id
    ).offset(offset).limit(limit).all()
    
    return tasks