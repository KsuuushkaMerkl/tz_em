from uuid import UUID
from pydantic import BaseModel, Field

from user.model import Role
from access.model import Action


class AccessRuleCreateSchema(BaseModel):
    role: Role
    resource: str = Field(min_length=1)
    action: Action


class AccessRuleUpdateSchema(BaseModel):
    role: Role | None = None
    resource: str | None = Field(default=None, min_length=1)
    action: Action | None = None


class AccessRuleResponseSchema(BaseModel):
    id: UUID
    role: Role
    resource: str
    action: Action

    class Config:
        from_attributes = True
