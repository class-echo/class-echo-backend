from sqlalchemy.orm import Session
from app import models, schemas
from datetime import datetime
from app.schemas import student_schema as student_schema


def create_student(db: Session, student: student_schema.StudentCreate):
    db_student = models.Student(
        school_id=student.school_id,
        f_name=student.f_name,
        l_name=student.l_name,
        address=student.address,
        admit_date=student.admit_date,
        leave_date=student.leave_date,
        created_at=datetime.utcnow()
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def get_student(db: Session, reg_no: int):
    return db.query(models.Student).filter(models.Student.reg_no == reg_no).first()

def get_students(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Student).offset(skip).limit(limit).all()

def update_student(db: Session, reg_no: int, student_update: student_schema.StudentUpdate):
    student = db.query(models.Student).filter(models.Student.reg_no == reg_no).first()
    if not student:
        return None
    for key, value in student_update.dict(exclude_unset=True).items():
        setattr(student, key, value)
    db.commit()
    db.refresh(student)
    return student

def delete_student(db: Session, reg_no: int):
    student = db.query(models.Student).filter(models.Student.reg_no == reg_no).first()
    if student:
        db.delete(student)
        db.commit()
    return student
