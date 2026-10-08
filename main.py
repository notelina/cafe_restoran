"""
УЧЕБНЫЙ СЕРВЕР: КАК РАБОТАЕТ КЛИЕНТ-СЕРВЕР

Что тут происходит:
1. Сервер принимает HTTP-запросы от браузера.
2. Валидирует данные через Pydantic.
3. Сохраняет в БД через SQLAlchemy.
4. Отдаёт HTML-страницу и JSON-ответы.

Каждый шаг логируется в консоль — чтобы ты видела, что происходит.
"""

from fastapi import FastAPI, Depends, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
import time

# Импорты из твоего проекта
from database import Base, engine, get_db
from models import Guest, Dish
from schemas import GuestCreate, GuestOut, DishCreate, DishOut
import crud

# === СОЗДАНИЕ ТАБЛИЦ В БД ===
# При запуске сервера SQLAlchemy создаёт таблицы, если их нет.
Base.metadata.create_all(bind=engine)

# === СОЗДАНИЕ ПРИЛОЖЕНИЯ ===
app = FastAPI(
    title="Учебный проект: клиент-сервер",
    description="Визуальный пример того, как данные ходят между браузером и сервером",
    version="1.0.0"
)


# === MIDDLEWARE: ЛОГИРОВАНИЕ КАЖДОГО ЗАПРОСА ===
# Это как «прослушка» — показывает, что браузер отправил и что сервер ответил.
@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Запоминаем время начала
    start = time.time()

    # Печатаем запрос
    print(f"\n{'=' * 60}")
    print(f"→ ЗАПРОС: {request.method} {request.url.path}")

    # Передаём запрос дальше (в эндпоинт)
    response = await call_next(request)

    # Считаем, сколько заняло
    duration = (time.time() - start) * 1000

    # Печатаем ответ
    print(f"← ОТВЕТ: {response.status_code} за {duration:.0f} мс")
    print(f"{'=' * 60}\n")

    return response


# === ГЛАВНАЯ СТРАНИЦА ===
# Когда ты открываешь http://127.0.0.1:8000/ — сервер отдаёт HTML-файл.
@app.get("/", tags=["Главная"])
def root():
    print("📄 [СЕРВЕР] Отдаю HTML-страницу клиенту")
    return FileResponse("static/index.html")


# === ЭНДПОИНТЫ ДЛЯ ГОСТЕЙ ===

@app.post("/guests", response_model=GuestOut, tags=["Гости"])
def create_guest(data: GuestCreate, db: Session = Depends(get_db)):
    """
    Создать нового гостя.

    Что происходит:
    1. FastAPI получает JSON от клиента.
    2. Pydantic (GuestCreate) валидирует данные и превращает в объект.
    3. CRUD создаёт объект Guest (SQLAlchemy).
    4. SQLAlchemy сохраняет в БД.
    5. FastAPI превращает объект в JSON (GuestOut).
    6. Отправляет ответ клиенту.
    """
    print(f"\n{'─' * 60}")
    print(f"📥 [СЕРВЕР] Получен JSON от клиента:")
    print(f"   {data}")
    print(f"🔄 [СЕРВЕР] Pydantic превратил JSON в объект GuestCreate")

    # Сохраняем в БД через CRUD
    guest = crud.create_guest(db, data)

    print(f"💾 [СЕРВЕР] SQLAlchemy сохранил в БД:")
    print(f"   id={guest.id}, name={guest.name}, number={guest.number}")
    print(f"📤 [СЕРВЕР] Отправляю ответ клиенту в формате JSON")
    print(f"{'─' * 60}\n")

    return guest


@app.get("/guests", response_model=List[GuestOut], tags=["Гости"])
def list_guests(db: Session = Depends(get_db)):
    """
    Получить список всех гостей.

    Что происходит:
    1. CRUD делает SELECT * FROM guests.
    2. SQLAlchemy возвращает список объектов Guest.
    3. FastAPI превращает их в JSON.
    4. Отправляет клиенту.
    """
    guests = crud.get_guests(db)
    print(f"📤 [СЕРВЕР] Отправляю {len(guests)} гостей клиенту")
    return guests


# === ЭНДПОИНТЫ ДЛЯ БЛЮД ===

@app.post("/dishes", response_model=DishOut, tags=["Блюда"])
def create_dish(data: DishCreate, db: Session = Depends(get_db)):
    """
    Создать новое блюдо.
    Работает так же, как создание гостя.
    """
    print(f"\n{'─' * 60}")
    print(f"📥 [СЕРВЕР] Получен JSON от клиента:")
    print(f"   {data}")

    dish = crud.create_dish(db, data)

    print(f"💾 [СЕРВЕР] Сохранено в БД:")
    print(f"   id={dish.id}, name={dish.name}, price={dish.price}")
    print(f"📤 [СЕРВЕР] Отправляю ответ клиенту")
    print(f"{'─' * 60}\n")

    return dish


@app.get("/dishes", response_model=List[DishOut], tags=["Блюда"])
def list_dishes(db: Session = Depends(get_db)):
    """Получить список всех блюд."""
    dishes = crud.get_dishes(db)
    print(f"📤 [СЕРВЕР] Отправляю {len(dishes)} блюд клиенту")
    return dishes

# === ПРОВЕРКА РАБОТЫ ===
# Когда ты открываешь http://127.0.0.1:8000/docs — видишь Swagger UI.
# Это автоматическая документация API.