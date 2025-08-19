from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import teacher_class_subject_schema
from app.crud import teacher_class_subject_crud
from app.database import get_db

router = APIRouter(prefix="/teacher-class-subject", tags=["Teacher Class Subject"])

@router.post("/", response_model=teacher_class_subject_schema.TeacherClassSubjectOut)
def create(mapping: teacher_class_subject_schema.TeacherClassSubjectCreate, db: Session = Depends(get_db)):
    result = teacher_class_subject_crud.create_teacher_class_subject(db, mapping)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/{tcs_id}", response_model=teacher_class_subject_schema.TeacherClassSubjectOut)
def read(tcs_id: int, db: Session = Depends(get_db)):
    mapping = teacher_class_subject_crud.get_teacher_class_subject(db, tcs_id)
    if not mapping:
        raise HTTPException(status_code=404, detail="Teacher Class Subject Mapping not found")
    return mapping

@router.get("/", response_model=list[teacher_class_subject_schema.TeacherClassSubjectOut])
def read_all(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return teacher_class_subject_crud.get_all_teacher_class_subjects(db, skip, limit)

@router.put("/{tcs_id}", response_model=teacher_class_subject_schema.TeacherClassSubjectOut)
def update(tcs_id: int, mapping_update: teacher_class_subject_schema.TeacherClassSubjectCreate, db: Session = Depends(get_db)):
    result = teacher_class_subject_crud.update_teacher_class_subject(db, tcs_id, mapping_update)
    if result is None:
        raise HTTPException(status_code=404, detail="Teacher Class Subject Mapping not found")
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.delete("/{tcs_id}", response_model=teacher_class_subject_schema.TeacherClassSubjectOut)
def delete(tcs_id: int, db: Session = Depends(get_db)):
    mapping = teacher_class_subject_crud.delete_teacher_class_subject(db, tcs_id)
    if not mapping:
        raise HTTPException(status_code=404, detail="Teacher Class Subject Mapping not found")
    return mapping
