"""init

Revision ID: 721d8c75faec
Revises: 
Create Date: 2022-07-14 21:24:05.203118

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '721d8c75faec'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('air',
                    sa.Column('id', sa.Integer, primary_key=True, index=True),
                    sa.Column('xgrowKey', sa.String, nullable=False),
                    sa.Column('airTemperature', sa.Integer, nullable=False),
                    sa.Column('airHumidity', sa.Integer, nullable=False),
                    sa.Column('airTemperatureLogList', sa.String, nullable=False),
                    sa.Column('airHumidityLogList', sa.String, nullable=False),

                    )


def downgrade():
    op.drop_table('air')
