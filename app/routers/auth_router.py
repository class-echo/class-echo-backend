from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user_schema import UserCreate, UserResponse, LoginRequest, GoogleSignupRequest
from app.crud import user_crud
from app.core.utils import verify_password, create_access_token
from app.config import settings
from app.models.user import UserRole 

from google.oauth2 import id_token
from google.auth.transport import requests

router = APIRouter(prefix="/auth", tags=["Auth"])

# ---------------- LOCAL AUTH ---------------- #

@router.post("/signup/local", response_model=UserResponse)
def signup_local(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_crud.create_user(db, user)


@router.post("/login/local")
def login_local(request: LoginRequest, db: Session = Depends(get_db)):
    user = user_crud.get_user_by_email(db, request.email)
    if not user or not verify_password(request.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"email": user.email, "role": user.role.value})
    return {"access_token": access_token, "token_type": "bearer"}


# ---------------- GOOGLE AUTH ---------------- #

@router.post("/signup/google", response_model=UserResponse)
def signup_google(request: GoogleSignupRequest, db: Session = Depends(get_db)):
    """
    Accepts Google ID token + role (first-time signup).
    """
    try:
        payload = id_token.verify_oauth2_token(
            request.id_token_str,
            requests.Request(),
            settings.GOOGLE_CLIENT_ID
        )
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Google token")

    email = payload.get("email")
    sub = payload.get("sub")  # unique Google user ID

    db_user = user_crud.get_user_by_email(db, email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user with Google auth
    user_data = UserCreate(
        email=email,
        password=None,
        role=request.role,
        school_id=None
    )
    new_user = user_crud.create_oauth_user(db, user_data, provider="google", oauth_sub=sub)

    return new_user


@router.post("/login/google")
def login_google(request: dict, db: Session = Depends(get_db)):
    """
    Accepts Google ID token and logs in the user.
    """
    id_token_str = request.get("id_token_str")
    if not id_token_str:
        raise HTTPException(status_code=400, detail="id_token_str is required")

    try:
        payload = id_token.verify_oauth2_token(
            id_token_str,
            requests.Request(),
            settings.GOOGLE_CLIENT_ID
        )
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Google token")

    email = payload.get("email")
    user = user_crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found. Please signup first.")

    access_token = create_access_token(data={"email": user.email, "role": user.role.value})
    return {"access_token": access_token, "token_type": "bearer"}
