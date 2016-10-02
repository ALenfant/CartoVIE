"""Change flag-like columns to Array

Revision ID: 3ccf842601be
Revises: 1ac2eca0f8b7
Create Date: 2016-09-27 23:37:50.421865

"""

from alembic import op
from sqlalchemy.dialects import postgresql
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ccf842601be'
down_revision = '1ac2eca0f8b7'
branch_labels = None
depends_on = None

FLAGS_FIELDS = ('required_education_level', 'required_education_type', 'required_languages', 'required_skills')


def upgrade():
    for column in FLAGS_FIELDS:
        op.alter_column('offers', column, type_=postgresql.ARRAY(sa.String()), existing_type=sa.String(),
                        postgresql_using="regexp_split_to_array(%s, ' +, +')" % column)


def downgrade():
    for column in FLAGS_FIELDS:
        op.alter_column('offers', column, type_=sa.String(), existing_type=postgresql.ARRAY(sa.String()),
                        postgresql_using="array_to_string(%s, ' , ')" % column)
