from fastapi import FastAPI
from app.database import Base, engine

app = FastAPI(title="School Transparency API")

# Auto-create tables (only for dev; use Alembic for production)
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"msg": "School backend is running"}
