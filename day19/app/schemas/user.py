from pydantic import BaseModel
#Schemas = API Contracts
class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    role: str

    class Config:
        from_attributes = True
