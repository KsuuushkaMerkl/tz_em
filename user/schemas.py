from uuid import UUID

from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    id: UUID
    surname: str
    name: str
    patronymic: str | None = None
    email: str = Field(pattern=r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
    password: str
    role: str
    is_active: bool


class LoginUserSchema(BaseModel):
    email: str = Field(pattern=r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
    password: str


class RegisterUserRequestSchema(BaseModel):
    surname: str
    name: str
    patronymic: str | None = None
    email: str = Field(pattern=r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
    password: str
    password_repeat: str


class UpdateUserRequestSchema(BaseModel):
    surname: str | None = None
    name: str | None = None
    patronymic: str | None = None
    email:  str | None = Field(default=None, min_length=1, pattern=r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
    password: str | None = None


class UpdateRoleUser(BaseModel):
    role: str


class UserResponseSchema(BaseModel):
    id: UUID
    surname: str
    name: str
    patronymic: str | None = None
    email: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True


class TokenResponseSchema(BaseModel):
    user_id: UUID
    access_token: str
    token_type: str = "bearer"
