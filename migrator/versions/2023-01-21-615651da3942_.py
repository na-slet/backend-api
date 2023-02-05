"""empty message

Revision ID: 615651da3942
Revises: 6e0c726108f6
Create Date: 2023-01-21 13:19:25.574930

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '615651da3942'
down_revision = '6e0c726108f6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('parent_first_name', sa.String(), nullable=True))
    op.add_column('users', sa.Column('parent_middle_name', sa.String(), nullable=True))
    op.add_column('users', sa.Column('parent_last_name', sa.String(), nullable=True))
    op.add_column('users', sa.Column('parent_email', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'parent_email')
    op.drop_column('users', 'parent_last_name')
    op.drop_column('users', 'parent_middle_name')
    op.drop_column('users', 'parent_first_name')
    # ### end Alembic commands ###
