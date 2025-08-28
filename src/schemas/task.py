from enum import Enum
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from typing import Optional

# Перечисление для статусов задачи
class TaskStatus(str, Enum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

# Базовая схема с общими полями
class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, json_schema_extra={"example": "Купить продукты"})
    description: Optional[str] = Field(None, max_length=500, json_schema_extra={"example": "Молоко, хлеб, сыр"})

# Схема для создания задачи (наследуется от базовой)
class TaskCreate(TaskBase):
    pass

# Схема для обновления задачи (все поля опциональны)
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    status: Optional[TaskStatus] = None

# Схема для возврата задачи из БД (наследуется от базовой, добавляет id и status)
class TaskInDB(TaskBase):
    id: UUID
    status: TaskStatus

    model_config = ConfigDict(from_attributes=True)

