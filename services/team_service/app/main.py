from fastapi import FastAPI

from app.api.v1.routers import team_router  # Импорт твоего роутера


app = FastAPI(
    title="Team Service",
    description="Сервис управления командами",
    version="1.0.0"
)

# Подключаем роутеры
app.include_router(team_router)


@app.get("/")
async def root():
    return {"message": "User Service is running"}