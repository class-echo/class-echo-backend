from sqlalchemy.orm import Session
from app import models
from app.schemas import subject_schema as schema

def create_subject(db: Session, subject: schema.SubjectCreate):
    # Check if school already exists
    school = db.query(models.School).filter(models.School.school_id == subject.school_id).first()
    if not school:
        return {"error": "School does not exist"}
    
    # Check if subject already exists in the school
    existing = db.query(models.Subject).filter(
        models.Subject.school_id == subject.school_id,
        models.Subject.subject_name == subject.subject_name
    ).first()

    if existing:
        return {"error": "Subject already exists in this school"}

    db_subject = models.Subject(**subject.model_dump())
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject

def get_subject(db: Session, subject_id: int):
    return db.query(models.Subject).filter(models.Subject.subject_id == subject_id).first()

def get_all_subjects(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Subject).offset(skip).limit(limit).all()

def update_subject(db: Session, subject_id: int, subject_update: schema.SubjectCreate):
    db_subject = get_subject(db, subject_id)
    if not db_subject:
        return None
    
    # Check if school already exists
    school = db.query(models.School).filter(models.School.school_id == subject_update.school_id).first()
    if not school:
        return {"error": "School does not exist"}

    # Prevent duplicate on update
    existing = db.query(models.Subject).filter(
        models.Subject.school_id == subject_update.school_id,
        models.Subject.subject_name == subject_update.subject_name,
        models.Subject.subject_id != subject_id  # Exclude current subject from check
    ).first()
    if existing:
        return {"error": "Subject with same name already exists in this school"}

    for key, value in subject_update.model_dump(exclude_unset=True).items():
        setattr(db_subject, key, value)

    db.commit()
    db.refresh(db_subject)
    return db_subject

def delete_subject(db: Session, subject_id: int):
    db_subject = get_subject(db, subject_id)
    if db_subject:
        db.delete(db_subject)
        db.commit()
    return db_subject
