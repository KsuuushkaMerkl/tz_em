import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import scoped_session

from core.db import get_session
from core.security import require_admin
from access.model import AccessRule
from access.schemas import (
    AccessRuleCreateSchema,
    AccessRuleUpdateSchema,
    AccessRuleResponseSchema,
)

router = APIRouter(prefix="/admin", tags=["admin-access"])


@router.get("/rules", response_model=list[AccessRuleResponseSchema])
async def list_rules(
    db: scoped_session = Depends(get_session),
    admin_user=Depends(require_admin),
):
    return db.query(AccessRule).order_by(AccessRule.resource, AccessRule.action).all()


@router.post("/rules", response_model=AccessRuleResponseSchema)
async def create_rule(
    request: AccessRuleCreateSchema,
    db: scoped_session = Depends(get_session),
    admin_user=Depends(require_admin),
):
    rule = AccessRule(role=request.role, resource=request.resource, action=request.action)

    db.add(rule)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Rule already exists or invalid data")

    db.refresh(rule)
    return rule


@router.patch("/rules/{rule_id}", response_model=AccessRuleResponseSchema)
async def update_rule(
    rule_id: uuid.UUID,
    request: AccessRuleUpdateSchema,
    db: scoped_session = Depends(get_session),
    admin_user=Depends(require_admin),
):
    rule = db.query(AccessRule).filter(AccessRule.id == rule_id).first()
    if rule is None:
        raise HTTPException(status_code=404, detail="Rule not found")

    data = request.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(rule, field, value)

    try:
        db.add(rule)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Rule update conflicts with existing rule")

    db.refresh(rule)
    return rule


@router.delete("/rules/{rule_id}")
async def delete_rule(
    rule_id: uuid.UUID,
    db: scoped_session = Depends(get_session),
    admin_user=Depends(require_admin),
):
    rule = db.query(AccessRule).filter(AccessRule.id == rule_id).first()
    if rule is None:
        raise HTTPException(status_code=404, detail="Rule not found")

    db.delete(rule)
    db.commit()
    return {"detail": "Rule deleted"}
