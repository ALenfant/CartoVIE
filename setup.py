import os
import sys

from sqlalchemy.sql.expression import text

import models
import settings
from database import Database
from models import Offer


def setup():
    if not check_python():
        print("This software needs Python 3.4 minimum")
        return
    print("Python version check OK")

    if not check_chmods():
        print("Please enable read and write access to", settings.PATH_CACHE_GEOCODER)
        return
    print("File permissions check OK")

    if not check_database():
        print("Please install PostgreSQL 9.5 and enable PostGIS")
        return
    print("PostgreSQL and PostGIS connection and version check OK")

    # if not create_tables():
    #     print("Impossible to create the database tables. Please check the error above")
    #     return
    # print("Database tables creation OK")

    print("Run ./alembic upgrade to proceed with the tables creation, then")
    print("everything's done! Run fetcher.py now then periodically to update your database!")


def check_python():
    return sys.version_info >= (3, 4)


def check_chmods():
    try:
        test_path = os.path.join(settings.PATH_CACHE_GEOCODER, "testfile")
        with open(test_path, "w") as file:
            file.write("Test")
        os.remove(test_path)
        return True
    except Exception as e:
        print("ERROR", e)
        return False


def check_database():
    try:
        database = Database()
        connection, metadata = database.connect()

        postgres_version = connection.execute(text("SHOW server_version;")).scalar().split('.')
        postgres_version = tuple(map(int, postgres_version))
        if postgres_version < (9, 5):
            return False

        postgis_version = connection.execute(text("SELECT PostGIS_Lib_Version();")).scalar().split('.')
        postgis_version = tuple(map(int, postgis_version))
        if postgis_version < (2, 2):
            return False

        return True
    except Exception as e:
        print("ERROR", e)
        return False


def create_tables():
    return #TODO remove
    database = Database()
    connection, metadata = database.connect()

    print(Offer.__table__)
    print(models.Base.metadata.create_all(connection))

if __name__ == "__main__":
    setup()
