from cassandra.cqlengine.connection import setup
from cassandra.cqlengine.models import Model as BaseModel
import re

setup(["127.0.0.1"], default_keyspace="labor")

class Model(BaseModel):
    __keyspace__ = "labor"
    __abstract__ = True

path = "/Users/jhaddad/datasets/labor/data/time.series/{}"

def parse_kv(suffix, first_field_len, skip_lines=2):
    """
    suffix is something like "ap/ap.area"
    """
    regex = "(.{{{}}})(.*)".format(first_field_len)
    parser = re.compile(regex)
    result = dict()

    with open(path.format(suffix)) as fp:
        for x in range(skip_lines):
            fp.next()

        for x in fp:
            x = x.strip()
            matches = parser.match(x)
            result[matches.group(1)] = matches.group(2).strip()

    return result
