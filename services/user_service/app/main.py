from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routers import user_router  # Импорт твоего роутера


app = FastAPI(
    title="User Service",
    description="Сервис управления пользователями",
    version="1.0.0"
)

# Подключаем роутеры
app.include_router(user_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем все источники, или указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы
    allow_headers=["*"],  # Разрешаем все заголовки
)

@app.get("/")
async def root():
    return {"message": "User Service is running"}