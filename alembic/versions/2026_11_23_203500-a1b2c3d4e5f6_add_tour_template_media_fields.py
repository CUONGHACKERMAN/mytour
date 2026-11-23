"""add tour template media fields

Revision ID: a1b2c3d4e5f6
Revises: 84ebea820e38
Create Date: 2026-11-23 20:35:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "84ebea820e38"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "tour_template",
        sa.Column("hero_image_url", sa.String(length=255), nullable=True),
        schema="tour",
    )
    op.add_column(
        "tour_template",
        sa.Column("gallery_image_urls", sa.Text(), nullable=True),
        schema="tour",
    )


def downgrade() -> None:
    op.drop_column("tour_template", "gallery_image_urls", schema="tour")
    op.drop_column("tour_template", "hero_image_url", schema="tour")
