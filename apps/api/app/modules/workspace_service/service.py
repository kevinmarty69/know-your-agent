import re
import unicodedata
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.errors import raise_http_error
from app.models.workspace import Workspace
from app.modules.audit_log.service import append_audit_event
from app.schemas.workspace import WorkspaceCreateRequest


def _slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_only = normalized.encode("ascii", "ignore").decode("ascii").lower()
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_only).strip("-")
    slug = re.sub(r"-{2,}", "-", slug)
    return slug


def create_workspace(db: Session, payload: WorkspaceCreateRequest) -> Workspace:
    slug = payload.slug or _slugify(payload.name)
    if not slug:
        raise_http_error(
            422,
            "WORKSPACE_SLUG_INVALID",
            "Unable to derive slug from name; provide an explicit slug",
        )

    existing = db.scalar(select(Workspace).where(Workspace.slug == slug))
    if existing is not None:
        raise_http_error(409, "WORKSPACE_SLUG_ALREADY_EXISTS", "Workspace slug already exists")

    workspace = Workspace(name=payload.name, slug=slug, status="active")
    db.add(workspace)
    db.flush()

    append_audit_event(
        db,
        workspace_id=workspace.id,
        event_type="workspace.created",
        subject_type="workspace",
        subject_id=workspace.id,
        event_data={
            "workspace_id": str(workspace.id),
            "name": workspace.name,
            "slug": workspace.slug,
        },
    )

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise_http_error(409, "WORKSPACE_SLUG_ALREADY_EXISTS", "Workspace slug already exists")

    db.refresh(workspace)
    return workspace


def get_workspace(db: Session, workspace_id: UUID) -> Workspace:
    workspace = db.scalar(select(Workspace).where(Workspace.id == workspace_id))
    if workspace is None:
        raise_http_error(404, "WORKSPACE_NOT_FOUND", "Workspace not found")
    return workspace
