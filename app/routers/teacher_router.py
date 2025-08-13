from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import teacher_schema
from app.crud import teacher_crud
from app.database import get_db

router = APIRouter(prefix="/teachers", tags=["Teachers"])

@router.post("/", response_model=teacher_schema.TeacherOut)
def create_teacher(teacher: teacher_schema.TeacherCreate, db: Session = Depends(get_db)):
    created_teacher = teacher_crud.create_teacher(db, teacher)
    if isinstance(created_teacher, dict) and "error" in created_teacher:
        raise HTTPException(status_code=400, detail=created_teacher["error"])
    return created_teacher

@router.get("/{teacher_id}", response_model=teacher_schema.TeacherOut)
def read_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher = teacher_crud.get_teacher(db, teacher_id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher

@router.get("/", response_model=list[teacher_schema.TeacherOut])
def read_all_teachers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return teacher_crud.get_teachers(db, skip, limit)

@router.put("/{teacher_id}", response_model=teacher_schema.TeacherOut)
def update_teacher(teacher_id: int, teacher_update: teacher_schema.TeacherCreate, db: Session = Depends(get_db)):
    updated_teacher = teacher_crud.update_teacher(db, teacher_id, teacher_update)
    if not updated_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    if isinstance(updated_teacher, dict) and "error" in updated_teacher:
        raise HTTPException(status_code=400, detail=updated_teacher["error"])
    return updated_teacher

@router.delete("/{teacher_id}")
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    deleted_teacher = teacher_crud.delete_teacher(db, teacher_id)
    if not deleted_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return {"message": "Teacher deleted successfully", "teacher": deleted_teacher}
