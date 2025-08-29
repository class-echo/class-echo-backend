from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import student_parent_schema
from app.crud import student_parent_crud
from app.database import get_db
from app.core.role_checker import RoleChecker, get_current_user
from app.models.user import User, UserRole

router = APIRouter(prefix="/student-parents", tags=["Student-Parents Mapping"])

# Admin-only access group
admin_roles = RoleChecker([UserRole.super_admin, UserRole.school_admin])


@router.post("/", response_model=student_parent_schema.StudentParentOut, dependencies=[Depends(admin_roles)])
def create_mapping(mapping: student_parent_schema.StudentParentCreate, db: Session = Depends(get_db)):
    """Admins create mapping"""
    result = student_parent_crud.create_student_parent(db, mapping)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.get("/{student_parent_id}", response_model=student_parent_schema.StudentParentOut)
def read_mapping(
    student_parent_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Admins can read any, parent/student only their own mapping"""
    mapping = student_parent_crud.get_student_parent(db, student_parent_id)
    if not mapping:
        raise HTTPException(status_code=404, detail="Student-Parents-Mapping not found")

    # RBAC logic
    if current_user.role in ["super_admin", "school_admin"]:
        return mapping

    if current_user.role == "parent":
        if mapping.parent and mapping.parent.email == current_user.email:
            return mapping

    if current_user.role == "student":
        if mapping.student and mapping.student.email == current_user.email:
            return mapping

    raise HTTPException(status_code=403, detail="Not authorized to view this mapping")


@router.get("/", response_model=list[student_parent_schema.StudentParentOut], dependencies=[Depends(admin_roles)])
def read_all_mappings(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Admins only"""
    return student_parent_crud.get_all_student_parents(db, skip, limit)


@router.put("/{student_parent_id}", response_model=student_parent_schema.StudentParentOut, dependencies=[Depends(admin_roles)])
def update_mapping(student_parent_id: int, update_data: student_parent_schema.StudentParentCreate, db: Session = Depends(get_db)):
    """Admins update mapping"""
    result = student_parent_crud.update_student_parent(db, student_parent_id, update_data)
    if not result:
        raise HTTPException(status_code=404, detail="Student-Parents-Mapping not found")
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.delete("/{student_parent_id}", response_model=student_parent_schema.StudentParentOut, dependencies=[Depends(admin_roles)])
def delete_mapping(student_parent_id: int, db: Session = Depends(get_db)):
    """Admins delete mapping"""
    mapping = student_parent_crud.delete_student_parent(db, student_parent_id)
    if not mapping:
        raise HTTPException(status_code=404, detail="Student-Parents-Mapping not found")
    return mapping
