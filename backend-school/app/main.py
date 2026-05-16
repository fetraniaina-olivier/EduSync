from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import engine, Base
from app.api.v1 import students, sync
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Créer les tables SQLite au démarrage
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="EduSync School Backend", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],  # Port du frontend école
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(students.router, prefix="/api/v1/students", tags=["Students"])
app.include_router(sync.router, prefix="/api/v1/sync", tags=["Sync"])

@app.get("/")
def root():
    return {"message": "School Backend is running", "docs": "/docs"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)