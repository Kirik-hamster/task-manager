import pytest
from fastapi.testclient import TestClient
from src.main import app

@pytest.fixture(scope="function")  # Для каждого теста создаем нового клиента
def test_client():
    """
    Фикстура предоставляет тестового клиента для FastAPI приложения.
    """
    with TestClient(app) as client:
        yield client

@pytest.fixture(autouse=True)  # Автоматически выполняется перед каждым тестом
def clean_test_database():
    """
    Фикстура очищает 'базу данных' перед каждым тестом.
    Это гарантирует изоляцию тестов друг от друга.
    """
    from src.services.task_service import _tasks_db
    _tasks_db.clear()
    yield
    # После теста тоже можно почистить, но autouse=True и так гарантирует очистку перед следующим