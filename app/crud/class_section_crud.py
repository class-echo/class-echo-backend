from sqlalchemy.orm import Session
from app.models.class_section import ClassSection
from app.schemas.class_section_schema import ClassSectionCreate

def create_class_section(db: Session, class_section: ClassSectionCreate):
    db_class_section = ClassSection(**class_section.model_dump())
    db.add(db_class_section)
    db.commit()
    db.refresh(db_class_section)
    return db_class_section

def get_class_sections(db: Session):
    return db.query(ClassSection).all()

def get_class_section(db: Session, class_section_id: int):
    return db.query(ClassSection).filter(ClassSection.class_section_id == class_section_id).first()

def delete_class_section(db: Session, class_section_id: int):
    db_class_section = get_class_section(db, class_section_id)
    if db_class_section:
        db.delete(db_class_section)
        db.commit()
    return db_class_section
