import pytest
from uuid import uuid4, UUID
from fastapi import status
from src.schemas.task import TaskStatus

def test_create_task_success(test_client):
    """
    Тест успешного создания задачи с валидными данными.
    Проверяет статус код, структуру ответа и значения полей.
    """
    # Arrange (Подготовка)
    task_data = {
        "title": "Изучить FastAPI",
        "description": "Пройти туториал и написать тестовое задание"
    }
    
    # Act (Действие)
    response = test_client.post("/tasks/", json=task_data)
    
    # Assert (Проверка)
    assert response.status_code == status.HTTP_201_CREATED
    
    response_data = response.json()
    assert "id" in response_data
    assert UUID(response_data["id"])  # Проверяем, что id валидный UUID
    assert response_data["title"] == task_data["title"]
    assert response_data["description"] == task_data["description"]
    assert response_data["status"] == TaskStatus.CREATED.value

def test_create_task_validation_errors(test_client):
    """
    Тест валидации входных данных при создании задачи.
    Проверяет различные кейсы невалидных данных.
    """
    # Пустой заголовок
    response = test_client.post("/tasks/", json={"title": ""})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    # Отсутствует обязательное поле title
    response = test_client.post("/tasks/", json={"description": "Без заголовка"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    # Слишком длинный заголовок
    long_title = "A" * 101  # Максимум 100 символов
    response = test_client.post("/tasks/", json={"title": long_title})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_get_task_success(test_client):
    """
    Тест успешного получения существующей задачи.
    """
    # Создаем задачу для теста
    create_response = test_client.post("/tasks/", json={"title": "Тестовая задача"})
    task_id = create_response.json()["id"]
    
    # Получаем задачу
    response = test_client.get(f"/tasks/{task_id}")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Тестовая задача"

def test_get_task_not_found(test_client):
    """
    Тест попытки получения несуществующей задачи.
    Должен возвращать 404 ошибку.
    """
    non_existent_id = uuid4()
    response = test_client.get(f"/tasks/{non_existent_id}")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Задача не найдена"

def test_get_tasks_empty(test_client):
    """
    Тест получения пустого списка задач.
    """
    response = test_client.get("/tasks/")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

def test_get_tasks_with_data(test_client):
    """
    Тест получения списка с несколькими задачами.
    """
    # Создаем несколько задач
    tasks_data = [
        {"title": "Задача 1", "description": "Описание 1"},
        {"title": "Задача 2", "description": "Описание 2"},
        {"title": "Задача 3"}  # Без описания
    ]
    
    created_tasks = []
    for task_data in tasks_data:
        response = test_client.post("/tasks/", json=task_data)
        created_tasks.append(response.json())
    
    # Получаем все задачи
    response = test_client.get("/tasks/")
    
    assert response.status_code == status.HTTP_200_OK
    tasks = response.json()
    
    assert len(tasks) == 3
    # Проверяем, что все созданные задачи присутствуют в ответе
    for created_task in created_tasks:
        assert any(task["id"] == created_task["id"] for task in tasks)

def test_update_task_success(test_client):
    """
    Тест успешного обновления задачи.
    Проверяет частичное обновление полей.
    """
    # Создаем задачу
    create_response = test_client.post("/tasks/", json={
        "title": "Исходный заголовок",
        "description": "Исходное описание"
    })
    task_id = create_response.json()["id"]
    
    # Обновляем только статус
    update_data = {"status": TaskStatus.IN_PROGRESS.value}
    response = test_client.patch(f"/tasks/{task_id}", json=update_data)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == TaskStatus.IN_PROGRESS.value
    assert data["title"] == "Исходный заголовок"  # Должно остаться неизменным
    assert data["description"] == "Исходное описание"  # Должно остаться неизменным
    
    # Обновляем несколько полей
    update_data = {
        "title": "Новый заголовок", 
        "description": "Новое описание"
    }
    response = test_client.patch(f"/tasks/{task_id}", json=update_data)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "Новый заголовок"
    assert data["description"] == "Новое описание"
    assert data["status"] == TaskStatus.IN_PROGRESS.value  # Должно остаться неизменным

def test_update_task_not_found(test_client):
    """
    Тест попытки обновления несуществующей задачи.
    """
    non_existent_id = uuid4()
    update_data = {"title": "Новое название"}
    
    response = test_client.patch(f"/tasks/{non_existent_id}", json=update_data)
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Задача не найдена"

def test_delete_task_success(test_client):
    """
    Тест успешного удаления задачи.
    """
    # Создаем задачу
    create_response = test_client.post("/tasks/", json={"title": "Задача для удаления"})
    task_id = create_response.json()["id"]
    
    # Удаляем задачу
    response = test_client.delete(f"/tasks/{task_id}")
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.content == b""  # Тело ответа должно быть пустым
    
    # Проверяем, что задача действительно удалена
    get_response = test_client.get(f"/tasks/{task_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_task_not_found(test_client):
    """
    Тест попытки удаления несуществующей задачи.
    """
    non_existent_id = uuid4()
    response = test_client.delete(f"/tasks/{non_existent_id}")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Задача не найдена"

def test_task_lifecycle(test_client):
    """
    Комплексный тест полного жизненного цикла задачи:
    создание → получение → обновление → удаление.
    """
    # 1. Создание
    create_data = {"title": "Полный цикл задачи", "description": "Тестовое описание"}
    create_response = test_client.post("/tasks/", json=create_data)
    assert create_response.status_code == status.HTTP_201_CREATED
    task_id = create_response.json()["id"]
    
    # 2. Получение после создания
    get_response = test_client.get(f"/tasks/{task_id}")
    assert get_response.status_code == status.HTTP_200_OK
    assert get_response.json()["status"] == TaskStatus.CREATED.value
    
    # 3. Обновление статуса
    update_response = test_client.patch(f"/tasks/{task_id}", json={"status": TaskStatus.IN_PROGRESS.value})
    assert update_response.status_code == status.HTTP_200_OK
    assert update_response.json()["status"] == TaskStatus.IN_PROGRESS.value
    
    # 4. Получение после обновления
    get_response = test_client.get(f"/tasks/{task_id}")
    assert get_response.status_code == status.HTTP_200_OK
    assert get_response.json()["status"] == TaskStatus.IN_PROGRESS.value
    
    # 5. Удаление
    delete_response = test_client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT
    
    # 6. Проверка, что задача удалена
    get_response = test_client.get(f"/tasks/{task_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND