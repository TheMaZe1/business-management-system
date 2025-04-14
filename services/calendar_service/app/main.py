import asyncio
from fastapi import FastAPI

from app.api.v1.routers import router
from app.utils.broker import start_calendar_event_listener  # Импорт твоего роутера


app = FastAPI(
    title="Calendar Service",
    description="Сервис управления календарем",
    version="1.0.0"
)

# Подключаем роутеры
app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Calendar Service is running"}

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_calendar_event_listener())