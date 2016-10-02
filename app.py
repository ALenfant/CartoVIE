import flask
import flask_restless
import flask_compress
from flask import json
from flask.json import JSONEncoder
from geoalchemy2.elements import WKBElement
from geoalchemy2.shape import to_shape
from geoalchemy2.functions import ST_AsGeoJSON

from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.functions import func

import models
from database import Database

database = Database()
engine, _ = database.connect()
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = scoped_session(Session)


class GeometryJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, WKBElement):
            point = to_shape(obj)
            return {"lng": point.x, "lat": point.y}
        return JSONEncoder.default(self, obj)

# Create the Flask application and the SQLAlchemy object.
app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.json_encoder = GeometryJSONEncoder

flask_compress.Compress(app)

# Create the Flask-Restless API manager.
manager = flask_restless.APIManager(app, session=session)

# Create API endpoints, which will be available at /api/<tablename> by
# default. Allowed HTTP methods can be specified as well.
def pre_get_many_light_offers(search_params=None, **kw):
    filters = search_params.get('filters', [])
    filters.append({"name": "active", "op": "==", "val": "false"})
    search_params['filters'] = filters
    return

manager.create_api(
    models.Offer,
    results_per_page=100,
)
manager.create_api(
    models.Offer,
    collection_name='offers_light',
    results_per_page=0,
    include_columns=['id', 'title', 'city', 'country', 'location'],
    preprocessors={
        'GET_MANY': [pre_get_many_light_offers],
    },
)

# start the flask loop
app.run()
