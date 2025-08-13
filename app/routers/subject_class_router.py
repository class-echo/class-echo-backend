from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import subject_class_schema
from app.crud import subject_class_crud
from app.database import get_db

router = APIRouter(prefix="/subject-class", tags=["Subject-Class Mapping"])

@router.post("/", response_model=subject_class_schema.SubjectClassOut)
def create(mapping: subject_class_schema.SubjectClassCreate, db: Session = Depends(get_db)):
    result = subject_class_crud.create_subject_class(db, mapping)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/{subject_class_id}", response_model=subject_class_schema.SubjectClassOut)
def read(subject_class_id: int, db: Session = Depends(get_db)):
    mapping = subject_class_crud.get_subject_class(db, subject_class_id)
    if not mapping:
        raise HTTPException(status_code=404, detail="Subject-Class Mapping not found")
    return mapping

@router.get("/", response_model=list[subject_class_schema.SubjectClassOut])
def read_all(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return subject_class_crud.get_all_subject_classes(db, skip, limit)

@router.put("/{subject_class_id}", response_model=subject_class_schema.SubjectClassOut)
def update(subject_class_id: int, mapping_update: subject_class_schema.SubjectClassCreate, db: Session = Depends(get_db)):
    result = subject_class_crud.update_subject_class(db, subject_class_id, mapping_update)
    if result is None:
        raise HTTPException(status_code=404, detail="Subject-Class Mapping not found")
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.delete("/{subject_class_id}", response_model=subject_class_schema.SubjectClassOut)
def delete(subject_class_id: int, db: Session = Depends(get_db)):
    mapping = subject_class_crud.delete_subject_class(db, subject_class_id)
    if not mapping:
        raise HTTPException(status_code=404, detail="Subject-Class Mapping not found")
    return mapping
