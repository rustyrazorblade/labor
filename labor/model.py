from cassandra.cqlengine.connection import setup
from cassandra.cqlengine.models import Model as BaseModel
from cassandra.cluster import Cluster
import re

setup(["127.0.0.1"], default_keyspace="labor")

class Model(BaseModel):
    __keyspace__ = "labor"
    __abstract__ = True

path = "/Users/jhaddad/datasets/labor/data/time.series/{}"

# create keyspace labor WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

def get_cluster():
    return Cluster(["127.0.0.1"])

def get_session():
    return get_cluster().connect("labor")
