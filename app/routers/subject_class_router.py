from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import subject_class_schema
from app.crud import subject_class_crud
from app.database import get_db
from app.core.role_checker import RoleChecker
from app.models.user import UserRole


router = APIRouter(prefix="/subject-class", tags=["Subject-Class Mapping"])

# Role dependencies
admin_roles = RoleChecker([UserRole.super_admin, UserRole.school_admin])
all_roles = RoleChecker([UserRole.super_admin, UserRole.school_admin, UserRole.teacher, UserRole.student])

@router.post("/", response_model=subject_class_schema.SubjectClassOut, dependencies=[Depends(admin_roles)])
def create(mapping: subject_class_schema.SubjectClassCreate, db: Session = Depends(get_db)):
    """
    Creates a new subject-class mapping.
    Only users with 'super_admin', 'school_admin' roles can access this endpoint.
    """
    result = subject_class_crud.create_subject_class(db, mapping)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/{subject_class_id}", response_model=subject_class_schema.SubjectClassOut, dependencies=[Depends(all_roles)])
def read(subject_class_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a single subject-class mapping by its ID.
    All authenticated users can access this endpoint.
    """
    mapping = subject_class_crud.get_subject_class(db, subject_class_id)
    if not mapping:
        raise HTTPException(status_code=404, detail="Subject-Class Mapping not found")
    return mapping

@router.get("/", response_model=list[subject_class_schema.SubjectClassOut], dependencies=[Depends(all_roles)])
def read_all(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieves a list of all subject-class mappings.
    All authenticated users can access this endpoint.
    """
    return subject_class_crud.get_all_subject_classes(db, skip, limit)

@router.put("/{subject_class_id}", response_model=subject_class_schema.SubjectClassOut, dependencies=[Depends(admin_roles)])
def update(subject_class_id: int, mapping_update: subject_class_schema.SubjectClassCreate, db: Session = Depends(get_db)):
    """
    Updates a subject-class mapping.
    Only users with 'super_admin', 'school_admin' roles can access this endpoint.
    """
    result = subject_class_crud.update_subject_class(db, subject_class_id, mapping_update)
    if result is None:
        raise HTTPException(status_code=404, detail="Subject-Class Mapping not found")
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.delete("/{subject_class_id}", response_model=subject_class_schema.SubjectClassOut, dependencies=[Depends(admin_roles)])
def delete(subject_class_id: int, db: Session = Depends(get_db)):
    """
    Deletes a subject-class mapping.
    Only users with 'super_admin' or 'school_admin' roles can access this endpoint.
    """
    mapping = subject_class_crud.delete_subject_class(db, subject_class_id)
    if not mapping:
        raise HTTPException(status_code=404, detail="Subject-Class Mapping not found")
    return mapping