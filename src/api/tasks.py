from fastapi import APIRouter, HTTPException, status
from uuid import UUID
from typing import List

from src.services.task_service import TaskService
from src.schemas.task import TaskCreate, TaskUpdate, TaskInDB

# Создаем роутер с префиксом /tasks и тегом для документации
router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=TaskInDB, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate):
    """
    Создание новой задачи.
    
    - **title**: Название задачи (обязательное)
    - **description**: Описание задачи (опциональное)
    """
    return await TaskService.create_task(task)

@router.get("/{task_id}", response_model=TaskInDB)
async def get_task(task_id: UUID):
    """
    Получение задачи по UUID.
    """
    task = await TaskService.get_task(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена"
        )
    return task

@router.get("/", response_model=List[TaskInDB])
async def get_tasks():
    """
    Получение списка всех задач.
    """
    return await TaskService.get_tasks()

@router.patch("/{task_id}", response_model=TaskInDB)
async def update_task(task_id: UUID, task_update: TaskUpdate):
    """
    Частичное обновление задачи.
    
    Можно обновить любое поле или несколько полей:
    - **title**: Новое название
    - **description**: Новое описание  
    - **status**: Новый статус (created, in_progress, completed)
    """
    updated_task = await TaskService.update_task(task_id, task_update)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена"
        )
    return updated_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: UUID):
    """
    Удаление задачи по UUID.
    """
    success = await TaskService.delete_task(task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена"
        )
    # При успешном удалении возвращаем статус 204 без тела ответа
    return None