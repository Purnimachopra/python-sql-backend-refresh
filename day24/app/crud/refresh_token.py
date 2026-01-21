from sqlalchemy.orm import Session
from datetime import datetime, timezone,timedelta
from app.models.refresh_token import RefreshToken

def create_refresh_token(db: Session, token: str, user_id: int, expires_at):
    db_token = RefreshToken(
        token=token,
        user_id=user_id,
        expires_at=expires_at
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token

def get_refresh_token(db: Session, token: str):
    return db.query(RefreshToken).filter(
        RefreshToken.token == token,
        RefreshToken.expires_at > datetime.now(timezone.utc)
    ).first()

def delete_refresh_token(db: Session, token: str):
    db.query(RefreshToken).filter(RefreshToken.token == token).delete()
    db.commit()
