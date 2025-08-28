from fastapi import FastAPI
from src.api import tasks

# Создаем экземпляр приложения FastAPI с метаданными для документации
app = FastAPI(
    title="Task Manager API",
    description="""REST API для управления задачами. 
    Поддерживает все CRUD операции: создание, чтение, обновление, удаление задач.""",
    version="1.0.0",
    contact={
        "name": "Мякотин Кирилл",
        "url": "https://github.com/Kirik-hamster",
    }
)

# Подключаем роутер с задачами
app.include_router(tasks.router)

@app.get("/", tags=["Root"])
async def root():
    """
    Корневой эндпоинт API.
    
    Возвращает приветственное сообщение и ссылку на документацию.
    """
    return {
        "message": "Добро пожаловать в Task Manager API!",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Проверка статуса работы API.
    
    Используется для мониторинга работоспособности сервиса.
    """
    return {"status": "healthy", "message": "Service is running normally"}