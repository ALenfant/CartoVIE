"""Add offers table

Revision ID: 2162eb4efbb8
Revises: 
Create Date: 2016-09-27 22:24:03.091334

"""

from alembic import op
import geoalchemy2
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2162eb4efbb8'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('offers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('country', sa.String(), nullable=True),
    sa.Column('city', sa.String(), nullable=True),
    sa.Column('start_date', sa.Date(), nullable=True),
    sa.Column('end_date', sa.Date(), nullable=True),
    sa.Column('duration_months', sa.Integer(), nullable=True),
    sa.Column('organization', sa.String(), nullable=True),
    sa.Column('salary', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('publication_date', sa.Date(), nullable=True),
    sa.Column('mission_type', sa.String(), nullable=True),
    sa.Column('jobs_availables', sa.Integer(), nullable=True),
    sa.Column('required_exerience_months', sa.Integer(), nullable=True),
    sa.Column('required_education_level', sa.String(), nullable=True),
    sa.Column('required_languages', sa.String(), nullable=True),
    sa.Column('required_skills', sa.String(), nullable=True),
    sa.Column('required_education_type', sa.String(), nullable=True),
    sa.Column('location', geoalchemy2.types.Geography(geometry_type='POINT', srid=4326), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('inserted_date', sa.DateTime(), nullable=True),
    sa.Column('updated_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_offers_location', 'offers', ['location'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_offers_location', table_name='offers')
    op.drop_table('offers')
    ### end Alembic commands ###