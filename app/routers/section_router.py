from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import section_schema
from app.crud import section_crud

router = APIRouter(prefix="/sections", tags=["Sections"])

@router.post("/", response_model=section_schema.SectionOut)
def create(section: section_schema.SectionCreate, db: Session = Depends(get_db)):
    return section_crud.create_section(db, section)

@router.get("/", response_model=list[section_schema.SectionOut])
def read_sections(db: Session = Depends(get_db)):
    return section_crud.get_sections(db)

@router.get("/{section_id}", response_model=section_schema.SectionOut)
def read_section(section_id: int, db: Session = Depends(get_db)):
    section = section_crud.get_section(db, section_id)
    if section is None:
        raise HTTPException(status_code=404, detail="Section not found")
    return section

@router.delete("/{section_id}")
def delete_section(section_id: int, db: Session = Depends(get_db)):
    section = section_crud.delete_section(db, section_id)
    if section is None:
        raise HTTPException(status_code=404, detail="Section not found")
    return {"message": "Section deleted"}
