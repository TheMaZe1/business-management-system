from fastapi import FastAPI

from app.api.v1.routers import user_router  # Импорт твоего роутера


app = FastAPI(
    title="User Service",
    description="Сервис управления пользователями",
    version="1.0.0"
)

# Подключаем роутеры
app.include_router(user_router)


@app.get("/")
async def root():
    return {"message": "User Service is running"}