from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import student_parent_schema
from app.crud import student_parent_crud
from app.database import get_db

router = APIRouter(prefix="/student-parents", tags=["Student-Parents-Mapping"])

@router.post("/", response_model=student_parent_schema.StudentParentOut)
def create_mapping(mapping: student_parent_schema.StudentParentCreate, db: Session = Depends(get_db)):
    result = student_parent_crud.create_student_parent(db, mapping)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/{student_parent_id}", response_model=student_parent_schema.StudentParentOut)
def read_mapping(student_parent_id: int, db: Session = Depends(get_db)):
    mapping = student_parent_crud.get_student_parent(db, student_parent_id)
    if not mapping:
        raise HTTPException(status_code=404, detail="Student-Parents-Mapping not found")
    return mapping

@router.get("/", response_model=list[student_parent_schema.StudentParentOut])
def read_all_mappings(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return student_parent_crud.get_all_student_parents(db, skip, limit)

@router.put("/{student_parent_id}", response_model=student_parent_schema.StudentParentOut)
def update_mapping(student_parent_id: int, update_data: student_parent_schema.StudentParentCreate, db: Session = Depends(get_db)):
    result = student_parent_crud.update_student_parent(db, student_parent_id, update_data)
    if not result:
        raise HTTPException(status_code=404, detail="Student-Parents-Mapping not found")
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.delete("/{student_parent_id}", response_model=student_parent_schema.StudentParentOut)
def delete_mapping(student_parent_id: int, db: Session = Depends(get_db)):
    mapping = student_parent_crud.delete_student_parent(db, student_parent_id)
    if not mapping:
        raise HTTPException(status_code=404, detail="Student-Parents-Mapping not found")
    return mapping