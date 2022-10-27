"""empty message

Revision ID: b7d5abf21638
Revises: 
Create Date: 2022-10-27 22:19:59.025581

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7d5abf21638'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bank',
    sa.Column('bank_id', sa.Integer(), nullable=False),
    sa.Column('reserve', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('bank_id')
    )
    op.create_table('user',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('login', sa.String(length=45), nullable=False),
    sa.Column('password', sa.String(length=45), nullable=False),
    sa.Column('full_name', sa.String(length=45), nullable=False),
    sa.Column('passport_number', sa.String(length=45), nullable=False),
    sa.Column('card_number', sa.String(length=45), nullable=False),
    sa.Column('bank_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['bank_id'], ['bank.bank_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('card_number'),
    sa.UniqueConstraint('login'),
    sa.UniqueConstraint('passport_number')
    )
    op.create_table('about_user',
    sa.Column('about_user_id', sa.Integer(), nullable=False),
    sa.Column('date_of_birth', sa.String(length=45), nullable=False),
    sa.Column('credit_history', sa.String(length=45), nullable=True),
    sa.Column('email', sa.String(length=45), nullable=True),
    sa.Column('phone_number', sa.String(length=45), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('about_user_id')
    )
    op.create_table('loan',
    sa.Column('loan_id', sa.Integer(), nullable=False),
    sa.Column('debt', sa.DECIMAL(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('loan_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('loan')
    op.drop_table('about_user')
    op.drop_table('user')
    op.drop_table('bank')
    # ### end Alembic commands ###
