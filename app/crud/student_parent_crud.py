from sqlalchemy.orm import Session
from app import models
from app.schemas import student_parent_schema

def create_student_parent(db: Session, mapping: student_parent_schema.StudentParentCreate):
    # Check School exists
    school = db.query(models.School).filter(models.School.school_id == mapping.school_id).first()
    if not school:
        return {"error": "School does not exist"}

    # Check Student exists in same school
    student = db.query(models.Student).filter(
        models.Student.reg_no == mapping.reg_no,
        models.Student.school_id == mapping.school_id
    ).first()
    if not student:
        return {"error": "Student does not exist in this school"}

    # Check Parent exists in same school
    parent = db.query(models.Parent).filter(
        models.Parent.parent_id == mapping.parent_id,
        models.Parent.school_id == mapping.school_id
    ).first()
    if not parent:
        return {"error": "Parent does not exist in this school"}

    # Prevent duplicate mapping
    existing_mapping = db.query(models.StudentParent).filter(
        models.StudentParent.reg_no == mapping.reg_no,
        models.StudentParent.parent_id == mapping.parent_id
    ).first()
    if existing_mapping:
        return {"error": "Mapping already exists"}

    db_mapping = models.StudentParent(**mapping.model_dump())
    db.add(db_mapping)
    db.commit()
    db.refresh(db_mapping)
    return db_mapping


def get_student_parent(db: Session, student_parent_id: int):
    return db.query(models.StudentParent).filter(
        models.StudentParent.student_parent_id == student_parent_id
    ).first()


def get_all_student_parents(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.StudentParent).offset(skip).limit(limit).all()


def update_student_parent(db: Session, student_parent_id: int, mapping_update: student_parent_schema.StudentParentCreate):
    db_mapping = get_student_parent(db, student_parent_id)
    if not db_mapping:
        return None

    # Validate again
    student = db.query(models.Student).filter(
        models.Student.reg_no == mapping_update.reg_no,
        models.Student.school_id == mapping_update.school_id
    ).first()
    if not student:
        return {"error": "Student does not exist in this school"}

    parent = db.query(models.Parent).filter(
        models.Parent.parent_id == mapping_update.parent_id,
        models.Parent.school_id == mapping_update.school_id
    ).first()
    if not parent:
        return {"error": "Parent does not exist in this school"}

    for key, value in mapping_update.model_dump(exclude_unset=True).items():
        setattr(db_mapping, key, value)
    db.commit()
    db.refresh(db_mapping)
    return db_mapping


def delete_student_parent(db: Session, student_parent_id: int):
    db_mapping = get_student_parent(db, student_parent_id)
    if db_mapping:
        db.delete(db_mapping)
        db.commit()
    return db_mapping