from fastapi import FastAPI
from fastapi.openapi.models import APIKey
from fastapi.openapi.utils import get_openapi

from app.db.base import Base
from app.db.session import engine
#from app.models.user import User

from app.api.v1.auth import router as auth_router
from app.api.v1.admin import router as admin_router
from app.api.v1.users import router as user_router
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(user_router)

# Custom OpenAPI to show simple Bearer token in Swagger
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Return-to-Work API",
        version="1.0.0",
        description="API for admin and users",
        routes=app.routes,
    )
    # Add global security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    # Apply to all endpoints
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi