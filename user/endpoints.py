import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import scoped_session

from core.config import settings
from core.db import get_session
from core.security import get_password_hash, verify_password, create_access_token, require_active_user, \
    ensure_self_or_admin, require_admin
from user.model import Role, User
from user.schemas import (
    LoginUserSchema,
    RegisterUserRequestSchema,
    TokenResponseSchema,
    UpdateRoleUser,
    UpdateUserRequestSchema,
    UserResponseSchema, UserSchema,
)

router = APIRouter()



@router.post("/auth/register")
async def register_user(
    request: RegisterUserRequestSchema,
    db: scoped_session = Depends(get_session),
):
    if request.password != request.password_repeat:
        raise HTTPException(status_code=400, detail="Passwords do not match.")

    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User is already registered.")

    data = request.model_dump()
    data.pop("password_repeat", None)
    data["hashed_password"] = get_password_hash(data.pop("password"))
    data["role"] = Role.base
    data["is_active"] = True

    new_user = User(**data)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id}


@router.post("/auth/login", response_model=TokenResponseSchema)
async def login_user(
    request: LoginUserSchema,
    db: scoped_session = Depends(get_session),
):
    user = db.query(User).filter(User.email == request.email).first()

    if user is None or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Пользователь не активен"
        )

    token = create_access_token(
        subject=str(user.id),
        expires_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    return TokenResponseSchema(
        access_token=token,
        token_type="bearer",
        user_id=user.id,
    )


@router.post("/update_user/{user_id}", response_model=UserResponseSchema)
async def update_user(
    user_id: uuid.UUID,
    request: UpdateUserRequestSchema,
    db: scoped_session = Depends(get_session),

    current_user: Annotated[User, Depends(require_active_user)] = None,
):
    ensure_self_or_admin(
        user_id=user_id,
        current_user=current_user
    )

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Пользователь не найден"
        )

    data = request.model_dump(exclude_unset=True)

    if "email" in data and data["email"] is not None:
        email_owner = db.query(User).filter(User.email == data["email"], User.id != user_id).first()
        if email_owner:
            raise HTTPException(
                status_code=400,
                detail="Email already in use"
            )

    if "hashed_password" in data and data["hashed_password"] is not None:
        data["hashed_password"] = get_password_hash(data["hashed_password"])

    for field, value in data.items():
        setattr(user, field, value)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/delete_user/{user_id}")
async def delete_user(
    user_id: uuid.UUID,
    db: scoped_session = Depends(get_session),
    current_user: Annotated[User, Depends(require_active_user)] = None,
):
    ensure_self_or_admin(user_id=user_id, current_user=current_user)

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    user.is_active = False

    db.add(user)
    db.commit()
    db.refresh(user)
    return {"detail": "Аккаунт деактивирован."}



@router.put("/admin/users/{user_id}/update_role", response_model=UserResponseSchema)
async def change_role(
    user_id: uuid.UUID,
    request: UpdateRoleUser,
    db: scoped_session = Depends(get_session),
    admin_user: Annotated[User, Depends(require_admin)] = None,
):

    try:
        new_role = Role(request.role)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Недопустимая роль. Используй: base/admin"
        )

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Пользователь не найден"
        )

    user.role = new_role
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
