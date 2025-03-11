"""Init

Revision ID: 9228e336fe84
Revises:
Create Date: 2025-03-11 22:36:11.560917

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9228e336fe84'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'password',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('service_name', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.LargeBinary(), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_password')),
        sa.UniqueConstraint(
            'service_name', name=op.f('uq_password_service_name')
        ),
    )
    op.create_index(op.f('ix_password_id'), 'password', ['id'], unique=True)



def downgrade() -> None:
    op.drop_index(op.f('ix_password_id'), table_name='password')
    op.drop_table('password')

