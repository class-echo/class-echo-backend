from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import student_schema
from app.crud import student_crud
from app.database import get_db
from app.core.role_checker import RoleChecker
from app.core.role_checker import get_current_user
from app.models.user import User, UserRole

router = APIRouter(prefix="/students", tags=["Students"])

# role dependencies
admin_roles = RoleChecker([UserRole.super_admin, UserRole.school_admin])
teacher_roles = RoleChecker([UserRole.super_admin, UserRole.school_admin, UserRole.teacher])
all_roles = RoleChecker([UserRole.super_admin, UserRole.school_admin, UserRole.teacher, UserRole.student])

@router.post("/", response_model=student_schema.StudentOut, dependencies=[Depends(teacher_roles)])
def create(student: student_schema.StudentCreate, db: Session = Depends(get_db)):
    return student_crud.create_student(db, student)

@router.get("/{reg_no}", response_model=student_schema.StudentOut, dependencies=[Depends(all_roles)])
def read(
    reg_no: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  
):
    student = student_crud.get_student(db, reg_no)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Restrict student to only their own record
    if current_user.role == "student":  # Fix: Use attribute access
        if current_user.email != student.email:
            raise HTTPException(status_code=403, detail="Not authorized to view this student")

    return student

@router.get("/", response_model=list[student_schema.StudentOut], dependencies=[Depends(teacher_roles)])
def read_all(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return student_crud.get_students(db, skip, limit)

@router.put("/{reg_no}", response_model=student_schema.StudentOut, dependencies=[Depends(teacher_roles)])
def update(reg_no: int, update_data: student_schema.StudentCreate, db: Session = Depends(get_db)):
    student = student_crud.update_student(db, reg_no, update_data)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.delete("/{reg_no}", response_model=student_schema.StudentOut, dependencies=[Depends(admin_roles)])
def delete(reg_no: int, db: Session = Depends(get_db)):
    student = student_crud.delete_student(db, reg_no)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student