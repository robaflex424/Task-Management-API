from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=200)
    priority: int = Field(gt=0, lt=6)
    due_date: datetime | None = None

class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, min_length=1, max_length=200)
    priority: int = Field(gt=0, lt=6)
    completed: bool | None = None
    due_date: datetime | None = None

    
class TaskResponse(BaseModel):
    id: int
    title: str 
    description: str 
    completed: bool
    priority: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)
    # allows to read data from objects with user.id, instead of user["id"]