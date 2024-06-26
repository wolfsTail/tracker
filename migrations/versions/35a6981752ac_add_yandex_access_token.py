"""add yandex access token

Revision ID: 35a6981752ac
Revises: caafd3e9317a
Create Date: 2024-05-18 11:38:30.838224

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '35a6981752ac'
down_revision: Union[str, None] = 'caafd3e9317a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Users', sa.Column('yandex_access_token', sa.String(), nullable=True))
    op.alter_column('Users', 'username',
               existing_type=sa.VARCHAR(length=64),
               nullable=True)
    op.alter_column('Users', 'password',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Users', 'password',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    op.alter_column('Users', 'username',
               existing_type=sa.VARCHAR(length=64),
               nullable=False)
    op.drop_column('Users', 'yandex_access_token')
    # ### end Alembic commands ###
