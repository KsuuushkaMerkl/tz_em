from sqlalchemy.orm import scoped_session

from core.config import settings
from core.security import get_password_hash
from user.model import User, Role


def create_default_admin(db: scoped_session) -> None:
    admin = db.query(User).filter(User.email == settings.ADMIN_EMAIL).first()
    if admin:
        return

    admin = User(
        surname=settings.ADMIN_SURNAME,
        name=settings.ADMIN_NAME,
        patronymic=settings.ADMIN_PATRONYMIC,
        email=settings.ADMIN_EMAIL,
        hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
        role=Role.admin,
        is_active=True,
    )

    db.add(admin)
    db.commit()
