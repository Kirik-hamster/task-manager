# Task Manager API

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

REST API для управления задачами с полным набором CRUD операций, построенное на FastAPI с использованием современных практик разработки.

## 🚀 Возможности

- **Полный CRUD функционал** для задач
- **Валидация данных** с помощью Pydantic v2
- **Автоматическая документация** Swagger/OpenAPI
- **Комплексное тестирование** с pytest (11 тестов, 100% покрытие)
- **Контейнеризация** с Docker
- **Чистая архитектура** с разделением на слои

## 📋 Модель данных

Задача включает следующие поля:
- `id` (UUID) - уникальный идентификатор
- `title` (str) - название задачи (1-100 символов)
- `description` (str, optional) - описание задачи (до 500 символов)
- `status` (enum) - статус задачи: `created`, `in_progress`, `completed`

## 🛠️ Технологический стек

- **Backend**: FastAPI (Python 3.13+)
- **Тестирование**: pytest + pytest-asyncio
- **Валидация**: Pydantic v2
- **Контейнеризация**: Docker
- **Документация**: Swagger/OpenAPI

## 📦 Установка и запуск

### Предварительные требования

- Python 3.13 или выше
- pip (менеджер пакетов Python)
- Docker (опционально, для контейнеризации)

### 1. Клонирование репозитория

```bash
git clone https://github.com/Kirik-hamster/task-manager
cd task_manager
```

### 2. Создание виртуального окружения

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# или
venv\Scripts\activate     # Windows
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Запуск приложения

```bash
uvicorn src.main:app --reload
```

Приложение будет доступно по адресу: http://localhost:8000

## 📚 Документация API

После запуска приложения доступна автоматическая документация:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Примеры запросов

#### Создание задачи
```bash
curl -X 'POST' \
  'http://localhost:8000/tasks/' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "Закончить тестовое задание",
  "description": "Написать код для менеджера задач"
}'
```

#### Получение всех задач
```bash
curl -X 'GET' 'http://localhost:8000/tasks/'
```

#### Обновление задачи
```bash
curl -X 'PATCH' \
  'http://localhost:8000/tasks/{task_id}' \
  -H 'Content-Type: application/json' \
  -d '{
  "status": "in_progress"
}'
```

## 🧪 Тестирование

### Запуск тестов

```bash
# Базовый запуск
pytest -v

# С подробным выводом
pytest -v --tb=short

# С измерением покрытия кода
pytest --cov=src --cov-report=term-missing
```

### Результаты тестирования

- ✅ **11 тестов** - все проходят успешно
- ✅ **100% покрытие** ключевой логики
- ✅ Позитивные и негативные сценарии
- ✅ Валидация входных данных
- ✅ Обработка ошибок

## 🐳 Запуск в Docker

### Сборка образа

```bash
docker build -t task-manager-api .
```

### Запуск контейнера

```bash
docker run -d -p 8000:8000 --name task_manager task-manager-api
```

### Остановка контейнера

```bash
docker stop task_manager
```

### Удалить контейнера

```bash
docker rm task_manager
```

## 📁 Структура проекта

```
task_manager/
├── src/                    # Исходный код приложения
│   ├── main.py            # Точка входа FastAPI
│   ├── models/            # Модели данных
│   ├── schemas/           # Pydantic схемы
│   ├── api/               # Эндпоинты API
│   └── services/          # Бизнес-логика
├── tests/                 # Тесты
│   ├── conftest.py        # Конфигурация pytest
│   └── test_tasks.py      # Тесты API
├── requirements.txt       # Зависимости Python
├── pytest.ini            # Конфигурация pytest
├── Dockerfile            # Конфигурация Docker
└── README.md             # Документация
```

## 🔧 API Endpoints

| Метод | Endpoint | Описание |
|-------|----------|----------|
| `POST` | `/tasks/` | Создание новой задачи |
| `GET` | `/tasks/` | Получение списка всех задач |
| `GET` | `/tasks/{task_id}` | Получение задачи по ID |
| `PATCH` | `/tasks/{task_id}` | Обновление задачи |
| `DELETE` | `/tasks/{task_id}` | Удаление задачи |
| `GET` | `/health` | Проверка статуса работы API |

## 🚀 Деплой

Приложение готово к деплою на различные платформы:

- **Docker** (любой хостинг с поддержкой Docker)
- **Railway** / **Render** / **Heroku**
- **Google Cloud Run** / **AWS ECS**
- **Любой VPS** с Python 3.13+

