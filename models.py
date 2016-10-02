from datetime import datetime
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.declarative.api import declarative_base, declared_attr
from sqlalchemy.sql.schema import Column, Index
from sqlalchemy.sql.sqltypes import Integer, String, Boolean, Date, DateTime
from geoalchemy2 import Geography

Base = declarative_base()


class Offer(Base):
    __tablename__ = 'offers'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    country = Column(String)
    city = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    duration_months = Column(Integer)
    organization = Column(String)
    salary = Column(Integer)
    description = Column(String)
    publication_date = Column(Date)
    mission_type = Column(String)
    jobs_availables = Column(Integer)
    required_experience_months = Column(Integer)
    required_education_level = Column(postgresql.ARRAY(String))
    required_languages = Column(postgresql.ARRAY(String))
    required_skills = Column(postgresql.ARRAY(String))
    required_education_type = Column(postgresql.ARRAY(String))

    active = Column(Boolean)
    inserted_date = Column(DateTime)
    updated_date = Column(DateTime)

    # Geographic fields need ugly hack to stop Alembic being weird https://github.com/geoalchemy/geoalchemy/issues/43
    location = Column(Geography(geometry_type='POINT', srid=4326, spatial_index=False))

    @declared_attr
    def __table_args__(cls):
        return (Index(
            'idx_{}_{}'.format(cls.__tablename__, 'location'), 'location', postgres_using='gist'
        ),)

    @staticmethod
    def upsert(conn, values):
        current_time = datetime.utcnow()

        update_values = values.copy()
        update_values['updated_date'] = current_time
        values['inserted_date'] = current_time

        statement = postgresql.insert(Offer)\
            .values(**values)\
            .on_conflict_do_update(
                index_elements=['id'],
                set_=update_values,
            )
        conn.execute(statement)

    def __repr__(self):
        return "<Offer(title='%s', city='%s')>" % (self.title, self.city)
