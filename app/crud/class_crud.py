from sqlalchemy.orm import Session
from app.models.class_section import Class
from app.schemas.class_schema import ClassCreate

def create_class(db: Session, class_: ClassCreate):
    db_class = Class(**class_.model_dump())
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    return db_class

def get_classes(db: Session):
    return db.query(Class).all()

def get_class(db: Session, class_id: int):
    return db.query(Class).filter(Class.class_id == class_id).first()

def delete_class(db: Session, class_id: int):
    db_class = get_class(db, class_id)
    if db_class:
        db.delete(db_class)
        db.commit()
    return db_class
