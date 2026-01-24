from sqlalchemy import Column, Integer, String, DateTime, ForeignKey,Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base import Base

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True)
    token = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    revoked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship(
        "User",
        back_populates="refresh_tokens"
    )