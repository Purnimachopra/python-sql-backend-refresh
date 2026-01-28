from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta

from app.models.refresh_token import RefreshToken
from app.core.security import generate_refresh_token, refresh_token_expiry


def create_refresh_token(db: Session, user_id: int) -> RefreshToken:
    token = generate_refresh_token()
    expires_at = refresh_token_expiry()
   # expires_at = datetime.now(timezone.utc) + timedelta(days=refresh_token_expiry)

    db_token = RefreshToken(
        token=token,
        user_id=user_id,
        expires_at=expires_at,
        revoked=False,
    )

    db.add(db_token)
    db.commit()
    db.refresh(db_token)

    return db_token


def get_refresh_token(db: Session, token: str) -> RefreshToken | None:
    return (
        db.query(RefreshToken)
        .filter(
            RefreshToken.token == token,
            RefreshToken.revoked.is_(False),
        )
        .first()
    )


def revoke_all_user_tokens(db: Session, user_id: int) -> None:
    db.query(RefreshToken).filter(
        RefreshToken.user_id == user_id,
        RefreshToken.revoked.is_(False),
    ).update({"revoked": True})
    db.commit()
