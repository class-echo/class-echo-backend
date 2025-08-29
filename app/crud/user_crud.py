from sqlalchemy.orm import Session
from app import models
from app.schemas.user_schema import UserCreate
from app.core.utils import hash_password  


def create_user(db: Session, user: UserCreate):
    db_user = models.User(
        email=user.email,
        password=hash_password(user.password),
        role=user.role,
        school_id=user.school_id,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()
