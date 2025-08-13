from sqlalchemy.orm import Session
from app import models
from app.schemas import teacher_schema as teacher_schema

def create_teacher(db: Session, teacher: teacher_schema.TeacherCreate):
    # Validate school exists
    school = db.query(models.School).filter(models.School.school_id == teacher.school_id).first()
    if not school:
        return {"error": "School does not exist"}

    db_teacher = models.Teacher(**teacher.model_dump())
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

def get_teacher(db: Session, teacher_id: int):
    return db.query(models.Teacher).filter(models.Teacher.teacher_id == teacher_id).first()

def get_teachers(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Teacher).offset(skip).limit(limit).all()

def update_teacher(db: Session, teacher_id: int, teacher_update: teacher_schema.TeacherCreate):
    db_teacher = get_teacher(db, teacher_id)
    if not db_teacher:
        return None

    # Validate school exists (if changed)
    if teacher_update.school_id != db_teacher.school_id:
        school = db.query(models.School).filter(models.School.school_id == teacher_update.school_id).first()
        if not school:
            return {"error": "School does not exist"}

    for key, value in teacher_update.model_dump(exclude_unset=True).items():
        setattr(db_teacher, key, value)

    db.commit()
    db.refresh(db_teacher)
    return db_teacher

def delete_teacher(db: Session, teacher_id: int):
    db_teacher = get_teacher(db, teacher_id)
    if db_teacher:
        db.delete(db_teacher)
        db.commit()
    return db_teacher
