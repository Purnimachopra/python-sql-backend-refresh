from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext

SECRET_KEY = "day20-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    if not isinstance(password, str):
        raise ValueError("Password must be a string")
    print("HASHING VALUE:", password)
    print("TYPE:", type(password))
    print("LENGTH:", len(password))
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


import secrets
from datetime import datetime, timedelta, timezone

def generate_refresh_token() -> str:
    return secrets.token_urlsafe(32)

def refresh_token_expiry():
    return datetime.now(timezone.utc) + timedelta(days=7)

def decode_access_token(token: str) -> dict:
    """
    Decode a JWT access token and return the payload.
    Raises JWTError if invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise ValueError(f"Invalid token: {str(e)}")