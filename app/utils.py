from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from app.config import settings  

# JWT settings
SECRET_KEY = settings.SECRET_KEY  
ALGORITHM = settings.ALGORITHM  
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES  

# -------- Password Hashing -------- #
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hashes password using bcrypt (via Passlib)."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies plain password against hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

# -------- JWT Token -------- #
def create_access_token(data: dict, expires_delta: int = None) -> str:
    """Creates JWT access token with expiration."""
    to_encode = data.copy()
    expire = datetime.now() + timedelta(
        minutes=expires_delta or ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
