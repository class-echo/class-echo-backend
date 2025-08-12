from sqlalchemy.orm import Session
from app import models
from app.schemas import parent_schema



def create_parent(db: Session, parent: parent_schema.ParentCreate):
    # Validate School exists
    school = db.query(models.School).filter(models.School.school_id == parent.school_id).first()
    if not school:
        return {"error": "School does not exist"}

    # Validate unique email
    existing_email = db.query(models.Parent).filter(models.Parent.email == parent.email).first()
    if existing_email:
        return {"error": "Parent with this email already exists"}

    db_parent = models.Parent(**parent.model_dump())
    db.add(db_parent)
    db.commit()
    db.refresh(db_parent)
    return db_parent


def get_parent(db: Session, parent_id: int):
    return db.query(models.Parent).filter(models.Parent.parent_id == parent_id).first()


def get_parents(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Parent).offset(skip).limit(limit).all()


def update_parent(db: Session, parent_id: int, parent_update: parent_schema.ParentCreate):
    db_parent = get_parent(db, parent_id)
    if not db_parent:
        return None

    # Validate School exists
    school = db.query(models.School).filter(models.School.school_id == parent_update.school_id).first()
    if not school:
        return {"error": "School does not exist"}

    for key, value in parent_update.model_dump(exclude_unset=True).items():
        setattr(db_parent, key, value)
    db.commit()
    db.refresh(db_parent)
    return db_parent


def delete_parent(db: Session, parent_id: int):
    db_parent = get_parent(db, parent_id)
    if db_parent:
        db.delete(db_parent)
        db.commit()
    return db_parent