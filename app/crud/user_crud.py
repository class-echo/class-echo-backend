from sqlalchemy.orm import Session
from app import models
from app.schemas.user_schema import UserCreate
from app.core.utils import hash_password  
from app.models.user import User, UserRole



def create_user(db: Session, user: UserCreate):
    """
    Create a local user (with password).
    """
    db_user = models.User(
        email=user.email,
        password=hash_password(user.password),
        role=UserRole(user.role),
        school_id=user.school_id,
        oauth_provider="local",
        oauth_sub=None
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_oauth_user(db: Session, user: UserCreate, provider: str, oauth_sub: str):
    """
    Create an OAuth user (Google, etc.) with no password.
    """
    db_user = models.User(
        email=user.email,
        password=None,  # No password for Google auth
        role=UserRole(user.role),
        school_id=user.school_id,
        oauth_provider=provider,
        oauth_sub=oauth_sub
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_oauth_sub(db: Session, provider: str, oauth_sub: str):
    """
    Fetch user via Google OAuth sub ID.
    """
    return (
        db.query(models.User)
        .filter(models.User.oauth_provider == provider, models.User.oauth_sub == oauth_sub)
        .first()
    )
