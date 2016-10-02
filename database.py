import sqlalchemy

import settings

__author__ = 'Antonin'


class Database:
    def __init__(self):
        pass

    def connect(self):
        url = self.get_connection_string()
        return self._connect(url)

    def get_connection_string(self):
        return self._create_connection_string(
            settings.DB_USER, settings.DB_PASSWORD,
            settings.DB_DATABASE,
            settings.DB_HOST, settings.DB_PORT)

    @staticmethod
    def _create_connection_string(user, password, db, host='localhost', port=5432):
        # We connect with the help of the PostgreSQL URL
        # postgresql://federer:grandestslam@localhost:5432/tennis
        url = 'postgresql://{}:{}@{}:{}/{}'
        return url.format(user, password, host, port, db)

    @staticmethod
    def _connect(url):
        """Returns a connection and a metadata object"""
        # The return value of create_engine() is our connection object
        engine = sqlalchemy.create_engine(url, client_encoding='utf8')

        # We then bind the connection to MetaData()
        meta = sqlalchemy.MetaData(bind=engine, reflect=True)

        return engine, meta
