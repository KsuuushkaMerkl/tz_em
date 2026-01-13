from fastapi import HTTPException, status
from sqlalchemy.orm import scoped_session

from access.model import AccessRule, Action
from user.model import User


def ensure_access(
    db: scoped_session,
    user: User,
    resource: str,
    action: Action,
) -> None:
    rule = (
        db.query(AccessRule)
        .filter(
            AccessRule.role == user.role,
            AccessRule.resource == resource,
            AccessRule.action == action,
        )
        .first()
    )

    if rule is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: no access rule for this action",
        )
