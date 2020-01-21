"""empty message

Revision ID: 2cc3b21c845f
Revises: 
Create Date: 2020-01-21 05:48:27.959337

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2cc3b21c845f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('channel',
    sa.Column('db_id', sa.Integer(), nullable=False),
    sa.Column('channel_id', sa.String(length=10), nullable=True),
    sa.Column('channel_name', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('db_id'),
    sa.UniqueConstraint('channel_id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), server_default='1', nullable=False),
    sa.Column('username', sa.String(length=24), nullable=True),
    sa.Column('more', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('message',
    sa.Column('db_id', sa.Integer(), nullable=False),
    sa.Column('message_id', sa.String(length=36), nullable=True),
    sa.Column('user_id', sa.String(length=20), nullable=True),
    sa.Column('ts', sa.Float(), nullable=False),
    sa.Column('reply_count', sa.Integer(), nullable=True),
    sa.Column('text', sa.Text(), nullable=True),
    sa.Column('channel_id', sa.String(length=10), nullable=False),
    sa.ForeignKeyConstraint(['channel_id'], ['channel.channel_id'], ),
    sa.PrimaryKeyConstraint('db_id')
    )
    op.create_table('reply',
    sa.Column('db_id', sa.Integer(), nullable=False),
    sa.Column('message_id', sa.String(length=36), nullable=True),
    sa.Column('user_id', sa.String(length=20), nullable=True),
    sa.Column('ts', sa.Float(), nullable=True),
    sa.Column('text', sa.Text(), nullable=True),
    sa.Column('thread_ts', sa.Float(), nullable=True),
    sa.Column('channel_id', sa.String(length=10), nullable=False),
    sa.ForeignKeyConstraint(['channel_id'], ['channel.channel_id'], ),
    sa.PrimaryKeyConstraint('db_id')
    )
    op.drop_table('messages')
    op.drop_table('garbage')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('garbage',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('text', sa.VARCHAR(length=25), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='garbage_pkey')
    )
    op.create_table('messages',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('text', sa.VARCHAR(length=25), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='messages_pkey')
    )
    op.drop_table('reply')
    op.drop_table('message')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_table('users')
    op.drop_table('channel')
    # ### end Alembic commands ###
