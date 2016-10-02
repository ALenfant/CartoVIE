import os

DB_HOST = 'localhost'
DB_DATABASE = 'cartovie'
DB_USER = 'cartovie'
DB_PASSWORD = ''
DB_PORT = 5432

PATH_APP = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
PATH_CACHE_GEOCODER = os.path.join(PATH_APP, 'cache/geocoding/')  # TODO chmod

API_KEY_GOOGLE_GEOCODER = ""
