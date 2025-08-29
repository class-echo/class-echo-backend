from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import teacher_schema
from app.crud import teacher_crud
from app.database import get_db
from app.core.role_checker import RoleChecker, get_current_user
from app.models.user import User, UserRole

router = APIRouter(prefix="/teachers", tags=["Teachers"])

# Role dependencies
admin_roles = RoleChecker([UserRole.super_admin, UserRole.school_admin])
all_roles = RoleChecker([UserRole.super_admin, UserRole.school_admin, UserRole.teacher, UserRole.student])
# Teacher-specific role dependency for reading their own record
teacher_specific_roles = RoleChecker([UserRole.super_admin, UserRole.school_admin, UserRole.teacher])

@router.post("/", response_model=teacher_schema.TeacherOut, dependencies=[Depends(admin_roles)])
def create_teacher(teacher: teacher_schema.TeacherCreate, db: Session = Depends(get_db)):
    """
    Creates a new teacher.
    Only users with 'super_admin' or 'school_admin' roles can access this endpoint.
    """
    created_teacher = teacher_crud.create_teacher(db, teacher)
    if isinstance(created_teacher, dict) and "error" in created_teacher:
        raise HTTPException(status_code=400, detail=created_teacher["error"])
    return created_teacher

@router.get("/{teacher_id}", response_model=teacher_schema.TeacherOut, dependencies=[Depends(teacher_specific_roles)])
def read_teacher(
    teacher_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieves a single teacher by ID.
    Super_admin, school_admin, and other teachers can view any teacher's record.
    A teacher can only view their own record.
    """
    teacher = teacher_crud.get_teacher(db, teacher_id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    # Restrict a teacher to only their own record
    if current_user.role == "teacher":
        if current_user.email != teacher.email:
            raise HTTPException(status_code=403, detail="Not authorized to view this teacher's record")

    return teacher

@router.get("/", response_model=list[teacher_schema.TeacherOut], dependencies=[Depends(admin_roles)])
def read_all_teachers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieves a list of all teachers.
    Only users with 'super_admin' or 'school_admin' roles can access this endpoint.
    """
    return teacher_crud.get_teachers(db, skip, limit)

@router.put("/{teacher_id}", response_model=teacher_schema.TeacherOut, dependencies=[Depends(admin_roles)])
def update_teacher(teacher_id: int, teacher_update: teacher_schema.TeacherCreate, db: Session = Depends(get_db)):
    """
    Updates a teacher's information.
    Only users with 'super_admin' or 'school_admin' roles can access this endpoint.
    """
    updated_teacher = teacher_crud.update_teacher(db, teacher_id, teacher_update)
    if not updated_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    if isinstance(updated_teacher, dict) and "error" in updated_teacher:
        raise HTTPException(status_code=400, detail=updated_teacher["error"])
    return updated_teacher

@router.delete("/{teacher_id}", dependencies=[Depends(admin_roles)])
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    """
    Deletes a teacher.
    Only users with 'super_admin' or 'school_admin' roles can access this endpoint.
    """
    deleted_teacher = teacher_crud.delete_teacher(db, teacher_id)
    if not deleted_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return {"message": "Teacher deleted successfully"}