"""Fixed corruption

Revision ID: 5a1eb2c8a297
Revises: bb912f2bc9b1
Create Date: 2025-03-25 00:42:15.375378

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5a1eb2c8a297'
down_revision: Union[str, None] = 'bb912f2bc9b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
