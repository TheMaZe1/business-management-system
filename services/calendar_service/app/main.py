from fastapi import FastAPI

from app.api.v1.routers import router  # Импорт твоего роутера


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