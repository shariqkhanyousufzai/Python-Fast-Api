from datetime import datetime
from pydantic import BaseModel, EmailStr, constr


class UserBaseSchema(BaseModel):
    name: str
    email: str
    photo: str
    phone: str
    role: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True

class UpdateUserSchema(BaseModel):
    name: str
    photo: str
    phone: str

    class Config:
        orm_mode = True

class CreateUserSchema(UserBaseSchema):
    password: constr(min_length=8)
    passwordConfirm: str
    verified: bool = False


class LoginUserSchema(BaseModel):
    email: EmailStr | None = "addy@gmail.com"
    password: constr(min_length=8) | None = "qwerty123"


class UserResponseSchema(UserBaseSchema):
    id: str
    pass


class UserResponse(BaseModel):
    status: str
    user: UserResponseSchema


class FindUserByEmail(BaseModel):
    email: EmailStr

class AccessFiles(BaseModel):
    image: str

