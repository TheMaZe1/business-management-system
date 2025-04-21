from fastapi import FastAPI

from app.api.v1.routers import router  # Импорт твоего роутера


app = FastAPI(
    title="Team Service",
    description="Сервис управления командами",
    version="1.0.0"
)

app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Team Service is running"}