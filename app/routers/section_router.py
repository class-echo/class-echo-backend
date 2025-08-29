from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import section_schema
from app.crud import section_crud
from app.core.role_checker import RoleChecker
from app.models.user import UserRole

router = APIRouter(prefix="/sections", tags=["Sections"])

# RBAC dependencies
admin_roles = RoleChecker([UserRole.super_admin, UserRole.school_admin])
view_roles = RoleChecker([UserRole.super_admin, UserRole.school_admin, UserRole.teacher, UserRole.student])


@router.post("/", response_model=section_schema.SectionOut, dependencies=[Depends(admin_roles)])
def create(section: section_schema.SectionCreate, db: Session = Depends(get_db)):
    """Only admins can create sections"""
    return section_crud.create_section(db, section)


@router.get("/", response_model=list[section_schema.SectionOut], dependencies=[Depends(view_roles)])
def read_sections(db: Session = Depends(get_db)):
    """All roles can view sections"""
    return section_crud.get_sections(db)


@router.get("/{section_id}", response_model=section_schema.SectionOut, dependencies=[Depends(view_roles)])
def read_section(section_id: int, db: Session = Depends(get_db)):
    """All roles can view a single section"""
    section = section_crud.get_section(db, section_id)
    if section is None:
        raise HTTPException(status_code=404, detail="Section not found")
    return section


@router.delete("/{section_id}", dependencies=[Depends(admin_roles)])
def delete_section(section_id: int, db: Session = Depends(get_db)):
    """Only admins can delete sections"""
    section = section_crud.delete_section(db, section_id)
    if section is None:
        raise HTTPException(status_code=404, detail="Section not found")
    return {"message": "Section deleted"}
