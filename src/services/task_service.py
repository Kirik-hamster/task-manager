from uuid import UUID, uuid4
from typing import Dict, List, Optional
from src.schemas.task import TaskInDB, TaskCreate, TaskUpdate, TaskStatus

# Временное хранилище данных в памяти
# В реальном приложении здесь будет работа с БД
_tasks_db: Dict[UUID, TaskInDB] = {}

class TaskService:
    """Сервис для работы с задачами (CRUD операции)"""
    
    @staticmethod
    async def create_task(task_create: TaskCreate) -> TaskInDB:
        """
        Создание новой задачи
        """
        task_id = uuid4()
        # Создаем объект задачи для хранения в БД
        task = TaskInDB(
            id=task_id,
            title=task_create.title,
            description=task_create.description,
            status=TaskStatus.CREATED
        )
        # Сохраняем в нашем "хранилище"
        _tasks_db[task_id] = task
        return task

    @staticmethod
    async def get_task(task_id: UUID) -> Optional[TaskInDB]:
        """
        Получение задачи по ID
        """
        return _tasks_db.get(task_id)

    @staticmethod
    async def get_tasks() -> List[TaskInDB]:
        """
        Получение списка всех задач
        """
        return list(_tasks_db.values())

    @staticmethod
    async def update_task(task_id: UUID, task_update: TaskUpdate) -> Optional[TaskInDB]:
        """
        Обновление задачи
        """
        task = _tasks_db.get(task_id)
        if not task:
            return None

        # Преобразуем обновления в словать, исключая не переданные поля
        update_data = task_update.model_dump(exclude_unset=True)
        
        # Создаем обновленную задачу
        updated_task = task.model_copy(update=update_data)
        
        # Сохраняем обновления
        _tasks_db[task_id] = updated_task
        return updated_task

    @staticmethod
    async def delete_task(task_id: UUID) -> bool:
        """
        Удаление задачи
        """
        if task_id in _tasks_db:
            del _tasks_db[task_id]
            return True
        return False