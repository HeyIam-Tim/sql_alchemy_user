"""empty message

Revision ID: a09c8e609a47
Revises: 
Create Date: 2024-07-25 13:55:31.695924

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a09c8e609a47'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vacancy',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=256), nullable=False),
    sa.Column('compensation', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('worker',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now() + interval '1 day')"), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('resume',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=256), nullable=False),
    sa.Column('compensation', sa.Integer(), nullable=False),
    sa.Column('workload', sa.Enum('parttime', 'fulltime', name='workload'), nullable=False),
    sa.Column('worker_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now() + interval '1 day')"), nullable=False),
    sa.CheckConstraint('compensation > 0', name='check_compensation_gt'),
    sa.ForeignKeyConstraint(['worker_id'], ['worker.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('title_index', 'resume', ['title'], unique=False)
    op.create_table('status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('resume_id', sa.Integer(), nullable=False),
    sa.Column('state', sa.Enum('active', 'inactive', 'pending', 'new', name='statusstates'), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now() + interval '1 day')"), nullable=False),
    sa.ForeignKeyConstraint(['resume_id'], ['resume.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vacancy_replies',
    sa.Column('resume_id', sa.Integer(), nullable=False),
    sa.Column('vacancy_id', sa.Integer(), nullable=False),
    sa.Column('cover_letter', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['resume_id'], ['resume.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['vacancy_id'], ['vacancy.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('resume_id', 'vacancy_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vacancy_replies')
    op.drop_table('status')
    op.drop_index('title_index', table_name='resume')
    op.drop_table('resume')
    op.drop_table('worker')
    op.drop_table('vacancy')
    op.execute("DROP TYPE")
    # ### end Alembic commands ###