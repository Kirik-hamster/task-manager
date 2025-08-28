from uuid import UUID, uuid4
from enum import Enum
from typing import Optional

# Внутренняя модель задачи (может использоваться для бизнес-логики)
class TaskStatus(str, Enum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Task:
    def __init__(
        self,
        title: str,
        description: Optional[str] = None,
        status: TaskStatus = TaskStatus.CREATED,
        id: Optional[UUID] = None
    ):
        self.id = id or uuid4()
        self.title = title
        self.description = description
        self.status = status