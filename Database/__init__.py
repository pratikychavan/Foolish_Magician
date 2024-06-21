import os

from datetime import datetime
from mongoengine import connect, register_connection, Document, DateTimeField

class DatabaseManager:
    def __init__(self, **kwargs):
        self.host = os.environ.get('MONGO_HOST', kwargs.get('host','localhost'))
        self.port = int(os.environ.get('MONGO_PORT', kwargs.get('port',27017)))
        self.username = os.environ.get('MONGO_USERNAME',kwargs.get('username','admin'))
        self.password = os.environ.get('MONGO_PASSWORD',kwargs.get('password','password'))
        self.app_name = os.environ.get('APP_NAME', kwargs.get('app_name','Foolish_Magician'))
        self.db_name = os.environ.get('DEFAULT_DB_NAME', kwargs.get('db_name','backend'))
        self._connection = None
        register_connection(
            alias=self.app_name,
            db=self.db_name,
            host=self.host, 
            port=self.port, 
            username=self.username, 
            password=self.password
        )
    
    def make_connection(self):
        self._connection = connect(
            alias=self.app_name
        )
    
    def get_connection(self, **kwargs):
        if self._connection is None:
            self.make_connection(self, **kwargs)
        return self._connection

    def close_connection(self):
        if self._connection is not None:
            self._connection.close()
            self._connection = None

class BaseModel(Document):
    meta = {"abstract": True}
    created_at = DateTimeField(default=datetime.now())
    updated_at = DateTimeField(default=datetime.now())

