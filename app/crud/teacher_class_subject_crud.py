from sqlalchemy.orm import Session
from app import models
from app.schemas import teacher_class_subject_schema

def create_teacher_class_subject(db: Session, mapping: teacher_class_subject_schema.TeacherClassSubjectCreate):
    # Validate teacher exists
    teacher = db.query(models.Teacher).filter(models.Teacher.teacher_id == mapping.teacher_id).first()
    if not teacher:
        return {"error": "Teacher does not exist"}

    # Validate subject exists
    subject = db.query(models.Subject).filter(models.Subject.subject_id == mapping.subject_id).first()
    if not subject:
        return {"error": "Subject does not exist"}

    # Validate class_section exists
    class_section = db.query(models.ClassSection).filter(models.ClassSection.class_section_id == mapping.class_section_id).first()
    if not class_section:
        return {"error": "Class section does not exist"}

    # Same school check
    if teacher.school_id != mapping.school_id or subject.school_id != mapping.school_id or class_section.school_id != mapping.school_id:
        return {"error": "School ID mismatch between teacher, subject, or class section"}

    # Prevent duplicate
    existing = db.query(models.TeacherClassSubject).filter(
        models.TeacherClassSubject.teacher_id == mapping.teacher_id,
        models.TeacherClassSubject.subject_id == mapping.subject_id,
        models.TeacherClassSubject.class_section_id == mapping.class_section_id,
        models.TeacherClassSubject.school_id == mapping.school_id
    ).first()
    if existing:
        return {"error": "This mapping already exists"}

    db_mapping = models.TeacherClassSubject(**mapping.model_dump())
    db.add(db_mapping)
    db.commit()
    db.refresh(db_mapping)
    return db_mapping

def get_teacher_class_subject(db: Session, tcs_id: int):
    return db.query(models.TeacherClassSubject).filter(models.TeacherClassSubject.teacher_class_subjects == tcs_id).first()

def get_all_teacher_class_subjects(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.TeacherClassSubject).offset(skip).limit(limit).all()

def update_teacher_class_subject(db: Session, tcs_id: int, mapping_update: teacher_class_subject_schema.TeacherClassSubjectCreate):
    db_mapping = get_teacher_class_subject(db, tcs_id)
    if not db_mapping:
        return None

    # Reuse same validations as create
    teacher = db.query(models.Teacher).filter(models.Teacher.teacher_id == mapping_update.teacher_id).first()
    if not teacher:
        return {"error": "Teacher does not exist"}

    subject = db.query(models.Subject).filter(models.Subject.subject_id == mapping_update.subject_id).first()
    if not subject:
        return {"error": "Subject does not exist"}

    class_section = db.query(models.ClassSection).filter(models.ClassSection.class_section_id == mapping_update.class_section_id).first()
    if not class_section:
        return {"error": "Class section does not exist"}

    if teacher.school_id != mapping_update.school_id or subject.school_id != mapping_update.school_id or class_section.school_id != mapping_update.school_id:
        return {"error": "School ID mismatch between teacher, subject, or class section"}

    existing = db.query(models.TeacherClassSubject).filter(
        models.TeacherClassSubject.teacher_id == mapping_update.teacher_id,
        models.TeacherClassSubject.subject_id == mapping_update.subject_id,
        models.TeacherClassSubject.class_section_id == mapping_update.class_section_id,
        models.TeacherClassSubject.school_id == mapping_update.school_id,
        models.TeacherClassSubject.teacher_class_subjects != tcs_id
    ).first()
    if existing:
        return {"error": "This mapping already exists"}

    for key, value in mapping_update.model_dump(exclude_unset=True).items():
        setattr(db_mapping, key, value)
    db.commit()
    db.refresh(db_mapping)
    return db_mapping

def delete_teacher_class_subject(db: Session, tcs_id: int):
    db_mapping = get_teacher_class_subject(db, tcs_id)
    if db_mapping:
        db.delete(db_mapping)
        db.commit()
    return db_mapping
