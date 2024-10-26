from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_active: bool = True


class UserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    hashed_credentials: str
    is_active: bool


class UserLogin(BaseModel):
    username: str
    password: str
