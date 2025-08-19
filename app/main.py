from fastapi import FastAPI
from app.database import Base, engine
from app.routers import class_section_router, school_router, student_router, class_router, section_router, student_class_router, parent_router, student_parent_router, teacher_router, subject_router, subject_class_router, teacher_class_subject_router


app = FastAPI(title="Class-Echo API")

# Auto-create tables (only for dev; use Alembic for production)
Base.metadata.create_all(bind=engine)

app.include_router(school_router.router)
app.include_router(student_router.router)
app.include_router(class_router.router)
app.include_router(section_router.router)
app.include_router(class_section_router.router)
app.include_router(student_class_router.router) 
app.include_router(parent_router.router) 
app.include_router(student_parent_router.router) 
app.include_router(teacher_router.router) 
app.include_router(subject_router.router) 
app.include_router(subject_class_router.router)
app.include_router(teacher_class_subject_router.router)

@app.get("/")
def read_root():
    return {"msg": "Class-Echo backend is running"}
