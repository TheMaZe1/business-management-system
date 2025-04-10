from fastapi import FastAPI

from app.api.routers import router

app = FastAPI(title="BMS")

app.include_router(router)