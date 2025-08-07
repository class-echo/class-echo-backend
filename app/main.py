from fastapi import FastAPI
from app.database import Base, engine
from app.routers import school_router, student_router, class_router


app = FastAPI(title="Class-Echo API")

# Auto-create tables (only for dev; use Alembic for production)
Base.metadata.create_all(bind=engine)

app.include_router(school_router.router)
app.include_router(student_router.router)
app.include_router(class_router.router)

@app.get("/")
def read_root():
    return {"msg": "School backend is running"}
