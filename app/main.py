from fastapi import FastAPI
from app.database import Base, engine
from app.routers import student


app = FastAPI(title="Class-Echo API")

# Auto-create tables (only for dev; use Alembic for production)
Base.metadata.create_all(bind=engine)

app.include_router(student.router)

@app.get("/")
def read_root():
    return {"msg": "School backend is running"}
