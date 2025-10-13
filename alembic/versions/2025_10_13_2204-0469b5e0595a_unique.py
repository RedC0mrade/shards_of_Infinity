"""unique

Revision ID: 0469b5e0595a
Revises: 5cfd8c1f1899
Create Date: 2025-10-13 22:04:55.249645

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0469b5e0595a"
down_revision: Union[str, Sequence[str], None] = "5cfd8c1f1899"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint(
        op.f("uq_player_card_instances_card_id"),
        "player_card_instances",
        type_="unique",
    )
    op.create_unique_constraint(
        "uq_game_card", "player_card_instances", ["game_id", "card_id"]
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("uq_game_card", "player_card_instances", type_="unique")
    op.create_unique_constraint(
        op.f("uq_player_card_instances_card_id"),
        "player_card_instances",
        ["card_id"],
        postgresql_nulls_not_distinct=False,
    )
