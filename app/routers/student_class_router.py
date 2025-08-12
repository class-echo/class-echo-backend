from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import student_class_schema as student_class_schema
from app.crud import student_class_crud as student_class_crud

router = APIRouter(prefix="/student-class", tags=["Student-Class Mapping"])

@router.post("/", response_model=student_class_schema.StudentClassOut)
def create(mapping: student_class_schema.StudentClassCreate, db: Session = Depends(get_db)):
    result = student_class_crud.create_student_class(db, mapping)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/{student_class_id}", response_model=student_class_schema.StudentClassOut)
def read(student_class_id: int, db: Session = Depends(get_db)):
    mapping = student_class_crud.get_student_class(db, student_class_id)
    if not mapping:
        raise HTTPException(status_code=404, detail="Student-Class mapping not found")
    return mapping

@router.get("/", response_model=list[student_class_schema.StudentClassOut])
def read_all(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return student_class_crud.get_all_student_classes(db, skip, limit)

@router.put("/{student_class_id}", response_model=student_class_schema.StudentClassOut)
def update(student_class_id: int, mapping_update: student_class_schema.StudentClassCreate, db: Session = Depends(get_db)):
    mapping = student_class_crud.update_student_class(db, student_class_id, mapping_update)
    if not mapping:
        raise HTTPException(status_code=404, detail="Student-Class mapping not found")
    return mapping

@router.delete("/{student_class_id}")
def delete(student_class_id: int, db: Session = Depends(get_db)):
    mapping = student_class_crud.delete_student_class(db, student_class_id)
    if not mapping:
        raise HTTPException(status_code=404, detail="Student-Class mapping not found")
    return {"message": "Student-Class mapping deleted successfully"}
