
from app.db.base_class import Base
from app.models.user import User
from app.models.refresh_token import RefreshToken



#   app.db.base must import all models (User, RefreshToken, etc.)
# This is non-negotiable for autogenerate to work.