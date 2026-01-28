from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, Field
from app.core.dependencies import get_db,get_current_user
from app.models.user import User
from app.models.refresh_token import RefreshToken
from datetime import datetime, timezone
from fastapi.security import OAuth2PasswordRequestForm

from app.db.session import SessionLocal
from app.core.security import get_password_hash, verify_password, create_access_token
from app.services.auth_tokens import create_refresh_token,revoke_all_user_tokens,get_refresh_token
from app.core.security import generate_refresh_token, refresh_token_expiry
from app.schemas.auth import TokenResponse,LogoutRequest,RefreshTokenRequest,UserCreate
router = APIRouter(prefix="/auth", tags=["auth"])
# current UTC time, timezone-aware
now_utc = datetime.now(timezone.utc)

    






@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):

     # 🔍 TEMPORARY DEBUG (VERY IMPORTANT)
    print("PASSWORD VA" \
    "LUE:", payload.password)
    print("PASSWORD TYPE:", type(payload.password))
    print("PASSWORD LENGTH:", len(payload.password.encode("utf-8")))
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=payload.email,
        hashed_password=get_password_hash(payload.password),
        role="admin",
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User registered successfully"}

@router.post("/login", response_model=TokenResponse)
def login(
    payload: UserCreate, db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    print("Incoming email:", payload.email)
    print("User found:", user is not None)
    if user:
        print("Stored hash:", user.hashed_password)
        print("Password valid:", verify_password(payload.password, user.hashed_password))
    access_token = create_access_token({"sub": str(user.id)})

    #refresh_token = generate_refresh_token()
    refresh_token = create_refresh_token(
        db=db,
        user_id=user.id
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token.token,
        "token_type": "bearer"
    }


@router.post("/refreshToken", response_model=TokenResponse)
def access_refresh_token(payload: RefreshTokenRequest, db: Session = Depends(get_db)):
    print("Incoming refresh token:", payload.refresh_token)
    tokens = db.query(RefreshToken).all()
    print("Tokens in DB:", [t.token for t in tokens])
    token_obj = get_refresh_token(db, payload.refresh_token)

    if not token_obj:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    if token_obj.expires_at.replace(tzinfo=timezone.utc) < now_utc:
        raise HTTPException(status_code=401, detail="Refresh token expired")

    if token_obj.revoked:
        # Token reuse detected
        revoke_all_user_tokens(db, token_obj.user_id)
        raise HTTPException(
            status_code=403,
            detail="Refresh token revoked. Possible token reuse detected."
        )

    # Rotate token
    token_obj.revoked = True
    db.commit()

    new_refresh = create_refresh_token(db, token_obj.user_id)
    access_token = create_access_token({"sub": str(token_obj.user_id)})

    return {
        "access_token": access_token,
        "refresh_token": new_refresh.token,
        "token_type": "bearer"
    }

@router.post("/logout")
def logout(
    payload: LogoutRequest,
    db: Session = Depends(get_db),
   current_user: User = Depends(get_current_user)
):
    print("inside logout")
    token_obj = get_refresh_token(db, payload.refresh_token)

   # print("Current user:", current_user.id)
    print("Refresh token user:", token_obj.user_id)
    if not token_obj or token_obj.user_id != current_user.id:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    token_obj.revoked = True
    db.commit()

    return {"message": "Logged out successfully"}
