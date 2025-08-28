# Alembic 初始迁移脚本
"""初始迁移

修订 ID: 0001_initial
上一次修订:
创建日期: 2024-01-01
"""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        "party",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("country", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_party_name", "party", ["name"], unique=False)

    op.create_table(
        "contract",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("party_id", sa.Integer(), nullable=False),
        sa.Column("currency", sa.String(), nullable=False, server_default="CNY"),
        sa.Column("amount_minor", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("version", sa.String(), nullable=False, server_default="0.1.0"),
        sa.Column("template_name", sa.String(), nullable=False, server_default="basic_zh"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("effective_date", sa.Date(), nullable=True),
        sa.Column("status", sa.String(), nullable=False, server_default="draft"),
        sa.Column("status_history", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("currency_rate", sa.Float(), nullable=False, server_default="1.0"),
        sa.ForeignKeyConstraint(["party_id"], ["party.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "contractfile",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("contract_id", sa.Integer(), nullable=False),
        sa.Column("kind", sa.String(), nullable=False),
        sa.Column("path", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["contract_id"], ["contract.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("contractfile")
    op.drop_table("contract")
    op.drop_index("ix_party_name", table_name="party")
    op.drop_table("party")
