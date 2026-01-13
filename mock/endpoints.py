from fastapi import APIRouter, Depends
from sqlalchemy.orm import scoped_session

from core.db import get_session
from core.security import require_active_user
from access.model import Action
from access.security import ensure_access
from user.model import User

router = APIRouter(prefix="/mock", tags=["mock-business"])

MOCK_OBJECTS = [
    {"id": 1, "title": "Object A"},
    {"id": 2, "title": "Object B"},
    {"id": 3, "title": "Object C"},
]


@router.get("/objects")
async def list_objects(
    db: scoped_session = Depends(get_session),
    current_user: User = Depends(require_active_user),
):
    ensure_access(db=db, user=current_user, resource="mock_objects", action=Action.read)
    return MOCK_OBJECTS


@router.get("/objects/{object_id}")
async def get_object(
    object_id: int,
    db: scoped_session = Depends(get_session),
    current_user: User = Depends(require_active_user),
):
    ensure_access(db=db, user=current_user, resource="mock_objects", action=Action.read)

    for obj in MOCK_OBJECTS:
        if obj["id"] == object_id:
            return obj

    return {"detail": "Not found"}
