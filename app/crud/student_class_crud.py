from sqlalchemy.orm import Session
from fastapi import HTTPException
from app import models
from app.schemas import student_class_schema as student_class_schema

def create_student_class(db: Session, mapping: student_class_schema.StudentClassCreate):
    #  Check if student exists in the same school
    student = db.query(models.Student).filter(
        models.Student.reg_no == mapping.reg_no,
        models.Student.school_id == mapping.school_id
    ).first()
    if not student:
        raise HTTPException(status_code=400, detail="Student does not exist in this school")

    #  Check if class_section exists in the same school
    class_section = db.query(models.ClassSection).filter(
        models.ClassSection.class_section_id == mapping.class_section_id,
        models.ClassSection.school_id == mapping.school_id
    ).first()
    if not class_section:
        raise HTTPException(status_code=400, detail="Class section does not exist in this school")

    #  Check if mapping already exists
    existing_mapping = db.query(models.StudentClass).filter(
        models.StudentClass.reg_no == mapping.reg_no,
        models.StudentClass.class_section_id == mapping.class_section_id
    ).first()
    if existing_mapping:
        raise HTTPException(status_code=400, detail="Mapping already exists for this student and class section")

    db_mapping = models.StudentClass(**mapping.model_dump())
    db.add(db_mapping)
    db.commit()
    db.refresh(db_mapping)
    return db_mapping


def get_student_class(db: Session, student_class_id: int):
    return db.query(models.StudentClass).filter(models.StudentClass.student_class_id == student_class_id).first()


def get_all_student_classes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.StudentClass).offset(skip).limit(limit).all()


def update_student_class(db: Session, student_class_id: int, mapping_update: student_class_schema.StudentClassCreate):
    db_mapping = get_student_class(db, student_class_id)
    if not db_mapping:
        return None

    #  Check if student exists in the same school
    student = db.query(models.Student).filter(
        models.Student.reg_no == mapping_update.reg_no,
        models.Student.school_id == mapping_update.school_id
    ).first()
    if not student:
        raise HTTPException(status_code=400, detail="Student does not exist in this school")

    #  Check if class_section exists in the same school
    class_section = db.query(models.ClassSection).filter(
        models.ClassSection.class_section_id == mapping_update.class_section_id,
        models.ClassSection.school_id == mapping_update.school_id
    ).first()
    if not class_section:
        raise HTTPException(status_code=400, detail="Class section does not exist in this school")

    #  Check if mapping already exists (and is not the same record being updated)
    existing_mapping = db.query(models.StudentClass).filter(
        models.StudentClass.reg_no == mapping_update.reg_no,
        models.StudentClass.class_section_id == mapping_update.class_section_id,
        models.StudentClass.student_class_id != student_class_id
    ).first()
    if existing_mapping:
        raise HTTPException(status_code=400, detail="Mapping already exists for this student and class section")

    # Apply updates
    for key, value in mapping_update.model_dump(exclude_unset=True).items():
        setattr(db_mapping, key, value)
    db.commit()
    db.refresh(db_mapping)
    return db_mapping


def delete_student_class(db: Session, student_class_id: int):
    db_mapping = get_student_class(db, student_class_id)
    if db_mapping:
        db.delete(db_mapping)
        db.commit()
    return db_mapping
