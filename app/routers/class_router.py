from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import class_schema
from app.crud import class_crud
from app.core.role_checker import RoleChecker
from app.models.user import UserRole

router = APIRouter(prefix="/classes", tags=["Classes"])

# RBAC role dependencies
admin_roles = RoleChecker([UserRole.super_admin, UserRole.school_admin])
view_roles = RoleChecker([UserRole.super_admin, UserRole.school_admin, UserRole.teacher, UserRole.student])


@router.post("/", response_model=class_schema.ClassOut, dependencies=[Depends(admin_roles)])
def create(class_: class_schema.ClassCreate, db: Session = Depends(get_db)):
    """Only admins can create new classes"""
    return class_crud.create_class(db, class_)


@router.get("/", response_model=list[class_schema.ClassOut], dependencies=[Depends(view_roles)])
def read_classes(db: Session = Depends(get_db)):
    """All roles can view classes"""
    return class_crud.get_classes(db)


@router.get("/{class_id}", response_model=class_schema.ClassOut, dependencies=[Depends(view_roles)])
def read_class(class_id: int, db: Session = Depends(get_db)):
    """All roles can view a single class"""
    class_ = class_crud.get_class(db, class_id)
    if class_ is None:
        raise HTTPException(status_code=404, detail="Class not found")
    return class_


@router.delete("/{class_id}", dependencies=[Depends(admin_roles)])
def delete_class(class_id: int, db: Session = Depends(get_db)):
    """Only admins can delete classes"""
    class_ = class_crud.delete_class(db, class_id)
    if class_ is None:
        raise HTTPException(status_code=404, detail="Class not found")
    return {"message": "Class deleted"}
