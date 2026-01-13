import enum
import uuid

from sqlalchemy import String, UUID, Boolean, Enum
from sqlalchemy.orm import mapped_column, Mapped

from core.base_model import Base


class Role(str, enum.Enum):
    base = "base"
    admin = "admin"


class User(Base):
    __tablename__ = 'users'  # noqa
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    surname: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    patronymic: Mapped[str] = mapped_column(String, nullable=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[Role] = mapped_column(Enum(Role, name="user_role"), default=Role.base, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
