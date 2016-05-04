from tsdb import DictDB, TSDBClient, TSDBStatus, TSDBServer
import timeseries as ts
import pytest


def identity(x):
    return x

schema = {
  'pk': {'convert': identity, 'index': None},  # will be indexed anyways
  'ts': {'convert': identity, 'index': None},
  'order': {'convert': int, 'index': 1},
  'blarg': {'convert': int, 'index': 1},
  'useless': {'convert': identity, 'index': None},
  'mean': {'convert': identity, 'index': None},
  'std': {'convert': identity, 'index': None},
}


def test_db_init():
    client = TSDBClient(25000, test=True)
    assert client.port == 25000
    return client


# def set_up_server():
#     db = DictDB(schema, 'pk')
#     server = TSDBServer(db, 25000)
#     return server

# does not actually send and receive messages from the server.
# Its just a mock test for now.
def test_client():
    client = test_db_init()
    # test adding triggers
    assert client.add_trigger('junk', 'insert_ts', None, 23) is None
    # test insert
    assert client.insert_ts('one', ts.TimeSeries([1, 2, 3], [1, 4, 9])) is None
    # test removing triggers
    assert client.remove_trigger('junk', 'insert_ts') is None
    # test upsert
    assert client.upsert_meta('one', {'order': 1, 'blarg': 1}) is None
    # test select
    assert client.select({'order': 1, 'blarg': 1}) == (TSDBStatus(0), {})

# set_up_server()
# test_client()
