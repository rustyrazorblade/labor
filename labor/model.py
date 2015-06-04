from cassandra.cqlengine.connection import setup
from cassandra.cqlengine.models import Model as BaseModel

setup(["127.0.0.1"], default_keyspace="labor")

class Model(BaseModel):
    __keyspace__ = "labor"
    __abstract__ = True

path = "/Users/jhaddad/datasets/labor/data/time.series/{}"
