"""initial

Revision ID: 50b22266f809
Revises: 
Create Date: 2026-04-26 00:48:46.977870

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector


# revision identifiers, used by Alembic.
revision = '50b22266f809'
down_revision = None
branch_labels = None
depends_on = None


def table_exists(table_name):
    bind = op.get_bind()
    inspector = Inspector.from_engine(bind)
    return table_name in inspector.get_table_names()


def upgrade():
    if not table_exists('user'):
        op.create_table('user',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password', sa.String(length=255), nullable=False),
        sa.Column('user_type', sa.String(length=20), nullable=False),
        sa.PrimaryKeyConstraint('user_id'),
        sa.UniqueConstraint('email')
        )

    if not table_exists('venue'):
        op.create_table('venue',
        sa.Column('venue_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('capacity', sa.Integer(), nullable=True),
        sa.Column('city', sa.String(length=255), nullable=True),
        sa.Column('state', sa.String(length=255), nullable=True),
        sa.Column('zip_code', sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint('venue_id')
        )

    if not table_exists('order'):
        op.create_table('order',
        sa.Column('order_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.Column('total_price', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('payment_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
        sa.PrimaryKeyConstraint('order_id')
        )

    if not table_exists('payment'):
        op.create_table('payment',
        sa.Column('payment_id', sa.Integer(), nullable=False),
        sa.Column('order_id', sa.Integer(), nullable=False),
        sa.Column('payment_method', sa.String(length=20), nullable=False),
        sa.Column('transaction_id', sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(['order_id'], ['order.order_id'], ),
        sa.PrimaryKeyConstraint('payment_id'),
        sa.UniqueConstraint('order_id')
        )

    if not table_exists('event'):
        op.create_table('event',
        sa.Column('event_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('time', sa.Time(), nullable=True),
        sa.Column('location_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['location_id'], ['venue.venue_id'], ),
        sa.PrimaryKeyConstraint('event_id')
        )

    if not table_exists('speaker'):
        op.create_table('speaker',
        sa.Column('speaker_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('event_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['event_id'], ['event.event_id'], ),
        sa.PrimaryKeyConstraint('speaker_id')
        )

    if not table_exists('ticket'):
        op.create_table('ticket',
        sa.Column('ticket_id', sa.Integer(), nullable=False),
        sa.Column('event_id', sa.Integer(), nullable=False),
        sa.Column('order_id', sa.Integer(), nullable=False),
        sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('type', sa.String(length=50), nullable=False),
        sa.Column('seat_number', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['event_id'], ['event.event_id'], ),
        sa.ForeignKeyConstraint(['order_id'], ['order.order_id'], ),
        sa.PrimaryKeyConstraint('ticket_id')
        )

    if not table_exists('tickettype'):
        op.create_table('tickettype',
        sa.Column('ticket_type_id', sa.Integer(), nullable=False),
        sa.Column('event_id', sa.Integer(), nullable=False),
        sa.Column('type', sa.String(length=50), nullable=False),
        sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['event_id'], ['event.event_id'], ),
        sa.PrimaryKeyConstraint('ticket_type_id')
        )


def downgrade():
    op.drop_table('tickettype')
    op.drop_table('ticket')
    op.drop_table('speaker')
    op.drop_table('event')
    op.drop_table('venue')
    op.drop_table('payment')
    op.drop_table('order')
    op.drop_table('user')
