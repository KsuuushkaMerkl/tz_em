import enum
import uuid

from sqlalchemy import Enum, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from core.base_model import Base
from user.model import Role


class Action(str, enum.Enum):
    read = "read"
    create = "create"
    update = "update"
    delete = "delete"


class AccessRule(Base):
    __tablename__ = "access_rule"  # noqa
    __table_args__ = (
        UniqueConstraint("role", "resource", "action", name="uq_rule_role_resource_action"),
    )
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role: Mapped[Role] = mapped_column(Enum(Role, name="user_role"), nullable=False)
    resource: Mapped[str] = mapped_column(String, nullable=False)
    action: Mapped[Action] = mapped_column(Enum(Action, name="action_type"), nullable=False)
