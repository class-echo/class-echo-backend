from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import teacher_class_subject_schema
from app.crud import teacher_class_subject_crud
from app.database import get_db
from app.core.role_checker import RoleChecker
from app.models.user import UserRole

router = APIRouter(prefix="/teacher-class-subject", tags=["Teacher Class Subject"])

# Role dependencies
admin_roles = RoleChecker([UserRole.super_admin, UserRole.school_admin])
all_roles = RoleChecker([UserRole.super_admin, UserRole.school_admin, UserRole.teacher, UserRole.student])

@router.post("/", response_model=teacher_class_subject_schema.TeacherClassSubjectOut, dependencies=[Depends(admin_roles)])
def create(mapping: teacher_class_subject_schema.TeacherClassSubjectCreate, db: Session = Depends(get_db)):
    """
    Creates a new teacher-class-subject mapping.
    Only users with 'super_admin' or 'school_admin' roles can access this endpoint.
    """
    result = teacher_class_subject_crud.create_teacher_class_subject(db, mapping)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/{tcs_id}", response_model=teacher_class_subject_schema.TeacherClassSubjectOut, dependencies=[Depends(all_roles)])
def read(tcs_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a single teacher-class-subject mapping by its ID.
    All authenticated users can access this endpoint.
    """
    mapping = teacher_class_subject_crud.get_teacher_class_subject(db, tcs_id)
    if not mapping:
        raise HTTPException(status_code=404, detail="Teacher Class Subject Mapping not found")
    return mapping

@router.get("/", response_model=list[teacher_class_subject_schema.TeacherClassSubjectOut], dependencies=[Depends(all_roles)])
def read_all(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieves a list of all teacher-class-subject mappings.
    All authenticated users can access this endpoint.
    """
    return teacher_class_subject_crud.get_all_teacher_class_subjects(db, skip, limit)

@router.put("/{tcs_id}", response_model=teacher_class_subject_schema.TeacherClassSubjectOut, dependencies=[Depends(admin_roles)])
def update(tcs_id: int, mapping_update: teacher_class_subject_schema.TeacherClassSubjectCreate, db: Session = Depends(get_db)):
    """
    Updates a teacher-class-subject mapping.
    Only users with 'super_admin' or 'school_admin' roles can access this endpoint.
    """
    result = teacher_class_subject_crud.update_teacher_class_subject(db, tcs_id, mapping_update)
    if result is None:
        raise HTTPException(status_code=404, detail="Teacher Class Subject Mapping not found")
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.delete("/{tcs_id}", response_model=teacher_class_subject_schema.TeacherClassSubjectOut, dependencies=[Depends(admin_roles)])
def delete(tcs_id: int, db: Session = Depends(get_db)):
    """
    Deletes a teacher-class-subject mapping.
    Only users with 'super_admin' or 'school_admin' roles can access this endpoint.
    """
    mapping = teacher_class_subject_crud.delete_teacher_class_subject(db, tcs_id)
    if not mapping:
        raise HTTPException(status_code=404, detail="Teacher Class Subject Mapping not found")
    return mapping