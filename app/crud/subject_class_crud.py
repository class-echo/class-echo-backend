from sqlalchemy.orm import Session
from app import models
from app.schemas import subject_class_schema

def create_subject_class(db: Session, mapping: subject_class_schema.SubjectClassCreate):
    # Validate subject exists
    subject = db.query(models.Subject).filter(models.Subject.subject_id == mapping.subject_id).first()
    if not subject:
        return {"error": "Subject does not exist"}

    # Validate class_section exists
    class_section = db.query(models.ClassSection).filter(models.ClassSection.class_section_id == mapping.class_section_id).first()
    if not class_section:
        return {"error": "Class section does not exist"}

    # Same school check
    if subject.school_id != mapping.school_id or class_section.school_id != mapping.school_id:
        return {"error": "School ID mismatch between subject/class section"}

    # Prevent duplicate mapping
    existing = db.query(models.SubjectClass).filter(
        models.SubjectClass.subject_id == mapping.subject_id,
        models.SubjectClass.class_section_id == mapping.class_section_id,
        models.SubjectClass.school_id == mapping.school_id
    ).first()
    if existing:
        return {"error": "Subject-Class Mapping already exists"}

    db_mapping = models.SubjectClass(**mapping.model_dump())
    db.add(db_mapping)
    db.commit()
    db.refresh(db_mapping)
    return db_mapping

def get_subject_class(db: Session, subject_class_id: int):
    return db.query(models.SubjectClass).filter(models.SubjectClass.subject_class_id == subject_class_id).first()

def get_all_subject_classes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.SubjectClass).offset(skip).limit(limit).all()

def update_subject_class(db: Session, subject_class_id: int, mapping_update: subject_class_schema.SubjectClassCreate):
    db_mapping = get_subject_class(db, subject_class_id)
    if not db_mapping:
        return None

    # Same validations as create
    subject = db.query(models.Subject).filter(models.Subject.subject_id == mapping_update.subject_id).first()
    if not subject:
        return {"error": "Subject does not exist"}

    class_section = db.query(models.ClassSection).filter(models.ClassSection.class_section_id == mapping_update.class_section_id).first()
    if not class_section:
        return {"error": "Class section does not exist"}

    if subject.school_id != mapping_update.school_id or class_section.school_id != mapping_update.school_id:
        return {"error": "School ID mismatch between subject/class section"}

    existing = db.query(models.SubjectClass).filter(
        models.SubjectClass.subject_id == mapping_update.subject_id,
        models.SubjectClass.class_section_id == mapping_update.class_section_id,
        models.SubjectClass.school_id == mapping_update.school_id,
        models.SubjectClass.subject_class_id != subject_class_id
    ).first()
    if existing:
        return {"error": "Subject-Class Mapping already exists"}

    for key, value in mapping_update.model_dump(exclude_unset=True).items():
        setattr(db_mapping, key, value)
    db.commit()
    db.refresh(db_mapping)
    return db_mapping

def delete_subject_class(db: Session, subject_class_id: int):
    db_mapping = get_subject_class(db, subject_class_id)
    if db_mapping:
        db.delete(db_mapping)
        db.commit()
    return db_mapping
