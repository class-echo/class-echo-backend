from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import subject_schema as subject_schema
from app.crud import subject_crud as crud
from app.database import get_db

router = APIRouter(prefix="/subjects", tags=["Subjects"])

@router.post("/", response_model=subject_schema.SubjectOut)
def create(subject: subject_schema.SubjectCreate, db: Session = Depends(get_db)):
    result = crud.create_subject(db, subject)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/{subject_id}", response_model=subject_schema.SubjectOut)
def read(subject_id: int, db: Session = Depends(get_db)):
    subject = crud.get_subject(db, subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject

@router.get("/", response_model=list[subject_schema.SubjectOut])
def read_all(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_all_subjects(db, skip, limit)

@router.put("/{subject_id}", response_model=subject_schema.SubjectOut)
def update(subject_id: int, update_data: subject_schema.SubjectCreate, db: Session = Depends(get_db)):
    result = crud.update_subject(db, subject_id, update_data)
    if result is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.delete("/{subject_id}", response_model=subject_schema.SubjectOut)
def delete(subject_id: int, db: Session = Depends(get_db)):
    subject = crud.delete_subject(db, subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject
