from fastapi import FastAPI
from app.core.config import settings
from app.core.cors import setup_cors
from app.api.v1.router import api_router
from app.db.init_db import init_db

app = FastAPI(title=settings.APP_NAME)

setup_cors(app)
app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/health")
async def health():
    return {"status": "ok"}
