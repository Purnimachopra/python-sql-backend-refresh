from sqlalchemy.orm import Session
from datetime import datetime, timezone,timedelta
from app.models.refresh_token import RefreshToken
#import uuid
import secrets

REFRESH_TOKEN_EXPIRE_DAYS = 7

#def create_refresh_token(db: Session, token: str, user_id: int, expires_at):
def create_refresh_token(db: Session, user_id: int):
    #token = str(uuid.uuid4())
    token = secrets.token_urlsafe(32)  # ← secure, URL-safe

    expires_at = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
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
    print("get_refresh_token")
    return db.query(RefreshToken).filter(
        RefreshToken.token == token,
        RefreshToken.expires_at > datetime.now(timezone.utc)
    ).first()

def delete_refresh_token(db: Session, token: str):
    db.query(RefreshToken).filter(RefreshToken.token == token).delete()
    db.commit()


def revoke_all_user_tokens(db: Session, user_id: int) -> int:
    """
    Revoke all active (non-revoked) refresh tokens for a user.
    Used when token reuse is detected or for forced logout.

    Returns:
        int: number of tokens revoked
    """
    revoked_count = (
        db.query(RefreshToken)
        .filter(
            RefreshToken.user_id == user_id,
            RefreshToken.revoked.is_(False)
        )
        .update(
            {"revoked": True},
            synchronize_session=False
        )
    )

    db.commit()
    return revoked_count