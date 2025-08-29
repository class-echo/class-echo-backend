from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import subject_schema as subject_schema
from app.crud import subject_crud as crud
from app.database import get_db
from app.core.role_checker import RoleChecker
from app.models.user import UserRole

router = APIRouter(prefix="/subjects", tags=["Subjects"])

# Role dependencies
admin_roles = RoleChecker([UserRole.super_admin, UserRole.school_admin])
all_roles = RoleChecker([UserRole.super_admin, UserRole.school_admin, UserRole.teacher, UserRole.student])

@router.post("/", response_model=subject_schema.SubjectOut, dependencies=[Depends(admin_roles)])
def create(subject: subject_schema.SubjectCreate, db: Session = Depends(get_db)):
    """
    Creates a new subject.
    Only users with 'super_admin', 'school_admin' roles can access this endpoint.
    """
    result = crud.create_subject(db, subject)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/{subject_id}", response_model=subject_schema.SubjectOut, dependencies=[Depends(all_roles)])
def read(subject_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a single subject by its ID.
    All authenticated users can access this endpoint.
    """
    subject = crud.get_subject(db, subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject

@router.get("/", response_model=list[subject_schema.SubjectOut], dependencies=[Depends(all_roles)])
def read_all(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieves a list of all subjects.
    All authenticated users can access this endpoint.
    """
    return crud.get_all_subjects(db, skip, limit)

@router.put("/{subject_id}", response_model=subject_schema.SubjectOut, dependencies=[Depends(admin_roles)])
def update(subject_id: int, update_data: subject_schema.SubjectCreate, db: Session = Depends(get_db)):
    """
    Updates a subject.
    Only users with 'super_admin', 'school_admin' roles can access this endpoint.
    """
    result = crud.update_subject(db, subject_id, update_data)
    if result is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.delete("/{subject_id}", response_model=subject_schema.SubjectOut, dependencies=[Depends(admin_roles)])
def delete(subject_id: int, db: Session = Depends(get_db)):
    """
    Deletes a subject.
    Only users with 'super_admin' or 'school_admin' roles can access this endpoint.
    """
    subject = crud.delete_subject(db, subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject