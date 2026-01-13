from sqlalchemy.orm import scoped_session

from access.model import AccessRule, Action
from user.model import Role


def seed_access_rules(db: scoped_session) -> None:
    rules = [
        (Role.base, "mock_objects", Action.read),
        (Role.admin, "mock_objects", Action.read),
        (Role.admin, "mock_objects", Action.create),
        (Role.admin, "mock_objects", Action.update),
        (Role.admin, "mock_objects", Action.delete),
    ]

    for role, resource, action in rules:
        exists = (
            db.query(AccessRule)
            .filter(AccessRule.role == role, AccessRule.resource == resource, AccessRule.action == action)
            .first()
        )
        if not exists:
            db.add(AccessRule(role=role, resource=resource, action=action))

    db.commit()
