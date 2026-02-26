"""sprint4 audit integrity indexes

Revision ID: 0002_sprint4_audit_idx
Revises: 0001_sprint0_init
Create Date: 2026-02-25 14:35:00
"""

import sqlalchemy as sa

from alembic import op

revision = "0002_sprint4_audit_idx"
down_revision = "0001_sprint0_init"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index(
        "ix_audit_events_workspace_time_desc_id_desc",
        "audit_events",
        ["workspace_id", sa.text("event_time DESC"), sa.text("id DESC")],
        unique=False,
    )
    op.create_index(
        "ix_audit_events_workspace_decision",
        "audit_events",
        ["workspace_id", sa.text("(event_data->>'decision')")],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_audit_events_workspace_decision", table_name="audit_events")
    op.drop_index("ix_audit_events_workspace_time_desc_id_desc", table_name="audit_events")
