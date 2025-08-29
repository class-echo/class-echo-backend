from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import student_class_schema
from app.crud import student_class_crud
from app.core.role_checker import get_current_user, RoleChecker
from app.models.user import User, UserRole

router = APIRouter(prefix="/student-class", tags=["Student-Class Mapping"])

# Admin-only dependency
admin_roles = RoleChecker([UserRole.super_admin, UserRole.school_admin])


@router.post("/", response_model=student_class_schema.StudentClassOut, dependencies=[Depends(admin_roles)])
def create(mapping: student_class_schema.StudentClassCreate, db: Session = Depends(get_db)):
    """Admins create mapping"""
    result = student_class_crud.create_student_class(db, mapping)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.get("/{student_class_id}", response_model=student_class_schema.StudentClassOut)
def read(student_class_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Admins can read any, student/parent only their own"""
    mapping = student_class_crud.get_student_class(db, student_class_id)
    if not mapping:
        raise HTTPException(status_code=404, detail="Student-Class mapping not found")

    # --- RBAC rules ---
    if current_user.role in ["super_admin", "school_admin"]:
        return mapping

    if current_user.role == "student":
        # check student's email in User table vs Student.email
        if mapping.student and mapping.student.email == current_user.email:
            return mapping

    if current_user.role == "parent":
        # check parent email in User table vs Parent.email (through student.parents relation)
        student = mapping.student
        if student and any(sp.parent.email == current_user.email for sp in student.parents):
            return mapping

    raise HTTPException(status_code=403, detail="Not authorized to view this mapping")


@router.get("/", response_model=list[student_class_schema.StudentClassOut], dependencies=[Depends(admin_roles)])
def read_all(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Admins only"""
    return student_class_crud.get_all_student_classes(db, skip, limit)


@router.put("/{student_class_id}", response_model=student_class_schema.StudentClassOut, dependencies=[Depends(admin_roles)])
def update(student_class_id: int, mapping_update: student_class_schema.StudentClassCreate, db: Session = Depends(get_db)):
    """Admins update mapping"""
    mapping = student_class_crud.update_student_class(db, student_class_id, mapping_update)
    if not mapping:
        raise HTTPException(status_code=404, detail="Student-Class mapping not found")
    return mapping


@router.delete("/{student_class_id}", dependencies=[Depends(admin_roles)])
def delete(student_class_id: int, db: Session = Depends(get_db)):
    """Admins delete mapping"""
    mapping = student_class_crud.delete_student_class(db, student_class_id)
    if not mapping:
        raise HTTPException(status_code=404, detail="Student-Class mapping not found")
    return {"message": "Student-Class mapping deleted successfully"}
