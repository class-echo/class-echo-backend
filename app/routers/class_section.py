from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import class_section_schema
from app.crud import class_section_crud as class_section_crud

router = APIRouter(prefix="/class-sections", tags=["Class Sections"])

@router.post("/", response_model=class_section_schema.ClassSectionOut)
def create_class_section(class_section: class_section_schema.ClassSectionCreate, db: Session = Depends(get_db)):
    return class_section_crud.create_class_section(db, class_section)

@router.get("/", response_model=list[class_section_schema.ClassSectionOut])
def get_class_sections(db: Session = Depends(get_db)):
    return class_section_crud.get_class_sections(db)

@router.get("/{class_section_id}", response_model=class_section_schema.ClassSectionOut)
def get_class_section(class_section_id: int, db: Session = Depends(get_db)):
    db_class_section = class_section_crud.get_class_section(db, class_section_id)
    if not db_class_section:
        raise HTTPException(status_code=404, detail="Class_Section not found")
    return db_class_section

@router.delete("/{class_section_id}", response_model=class_section_schema.ClassSectionOut)
def delete_class_section(class_section_id: int, db: Session = Depends(get_db)):
    db_class_section = class_section_crud.delete_class_section(db, class_section_id)
    if not db_class_section:
        raise HTTPException(status_code=404, detail="Class_Section not found")
    return {"message": "Class_Section deleted successfully", "class_section": db_class_section}
