from sqlalchemy.orm import Session
from app.models.school import School
from app.schemas.school_schema import SchoolCreate

def create_school(db: Session, school: SchoolCreate):
    db_school = School(school_name=school.school_name)
    db.add(db_school)
    db.commit()
    db.refresh(db_school)
    return db_school

def get_school(db: Session, school_id: int):
    return db.query(School).filter(School.school_id == school_id).first()

def get_all_schools(db: Session, skip: int = 0, limit: int = 10):
    return db.query(School).offset(skip).limit(limit).all()

def delete_school(db: Session, school_id: int):
    db_school = db.query(School).filter(School.school_id == school_id).first()
    if db_school:
        db.delete(db_school)
        db.commit()
    return db_school

def update_school(db: Session, school_id: int, school: SchoolCreate):
    db_school = db.query(School).filter(School.school_id == school_id).first()
    if db_school:
        db_school.school_name = school.school_name
        db.commit()
        db.refresh(db_school)
    return db_school