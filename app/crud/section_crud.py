from sqlalchemy.orm import Session
from app.models.class_section import Section
from app.schemas.section_schema import SectionCreate

def create_section(db: Session, section: SectionCreate):
    db_section = Section(**section.model_dump())
    db.add(db_section)
    db.commit()
    db.refresh(db_section)
    return db_section

def get_sections(db: Session):
    return db.query(Section).all()

def get_section(db: Session, section_id: int):
    return db.query(Section).filter(Section.section_id == section_id).first()

def delete_section(db: Session, section_id: int):
    db_section = get_section(db, section_id)
    if db_section:
        db.delete(db_section)
        db.commit()
    return db_section
