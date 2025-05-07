from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.db import init_db
from app.api.routes import meal_planner
from app.api.routes import grocery
from app.api.routes import search

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Meal Planner API", description="API for meal planning", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # TODO: Change to only allow localhost
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(meal_planner.router, prefix="/api/v1")
app.include_router(grocery.router, prefix="/api/v1")
app.include_router(search.router, prefix="/api/v1")
@app.get("/health")
async def health_check():
    return {"status": "ok"}