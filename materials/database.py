from flask import g
from pymongo import MongoClient
from werkzeug.local import LocalProxy
from materials import app

def get_db():
    client = getattr(g, '_client', None)
    if client is None:
        client = g._client = MongoClient(app.config['DB_URI'],
                             connectTimeoutMS=30000,
                             socketTimeoutMS=None)
    db = client.get_database()
    return db

@app.teardown_appcontext
def teardown_db(exception):
    client = getattr(g, '_client', None)
    if client is not None:
        client.close()

db = LocalProxy(get_db)
