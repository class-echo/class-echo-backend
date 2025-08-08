from fastapi import FastAPI
from app.database import Base, engine
from app.routers import school_router, student_router, class_router, section_router, class_section


app = FastAPI(title="Class-Echo API")

# Auto-create tables (only for dev; use Alembic for production)
Base.metadata.create_all(bind=engine)

app.include_router(school_router.router)
app.include_router(student_router.router)
app.include_router(class_router.router)
app.include_router(section_router.router)
app.include_router(class_section.router)

@app.get("/")
def read_root():
    return {"msg": "Class-Echo backend is running"}
