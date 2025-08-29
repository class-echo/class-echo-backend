from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import class_section_schema
from app.crud import class_section_crud
from app.core.role_checker import RoleChecker
from app.models.user import UserRole

router = APIRouter(prefix="/class-sections", tags=["Class Sections"])

# RBAC
admin_roles = RoleChecker([UserRole.super_admin, UserRole.school_admin])
view_roles = RoleChecker([UserRole.super_admin, UserRole.school_admin, UserRole.teacher, UserRole.student])


@router.post("/", response_model=class_section_schema.ClassSectionOut, dependencies=[Depends(admin_roles)])
def create_class_section(class_section: class_section_schema.ClassSectionCreate, db: Session = Depends(get_db)):
    """Only admins can create class-section"""
    db_class_section = class_section_crud.create_class_section(db, class_section)
    return db_class_section


@router.get("/", response_model=list[class_section_schema.ClassSectionOut], dependencies=[Depends(view_roles)])
def get_class_sections(db: Session = Depends(get_db)):
    """All roles can view all class-sections"""
    return class_section_crud.get_class_sections(db)


@router.get("/{class_section_id}", response_model=class_section_schema.ClassSectionOut, dependencies=[Depends(view_roles)])
def get_class_section(class_section_id: int, db: Session = Depends(get_db)):
    """All roles can view a specific class-section"""
    db_class_section = class_section_crud.get_class_section(db, class_section_id)
    if not db_class_section:
        raise HTTPException(status_code=404, detail="Class_Section not found")
    return db_class_section


@router.delete("/{class_section_id}",response_model=None, dependencies=[Depends(admin_roles)])
def delete_class_section(class_section_id: int, db: Session = Depends(get_db)):
    """Only admins can delete class-section"""
    db_class_section = class_section_crud.delete_class_section(db, class_section_id)
    if not db_class_section:
        raise HTTPException(status_code=404, detail="Class_Section not found")
    return {"message": "Class_Section deleted successfully"}
