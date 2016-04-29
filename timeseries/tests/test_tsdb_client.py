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
    client = TSDBClient(25000)
    assert client.port == 25000
    return client


# def set_up_server():
#     db = DictDB(schema, 'pk')
#     server = TSDBServer(db, 25000)
#     server.run()


# def test_client():
#     client = test_db_init()
#     # test adding triggers
#     client.add_trigger('junk', 'insert_ts', None, 23)
#     # test insert
#     client.insert_ts('one', ts.TimeSeries([1, 2, 3], [1, 4, 9]))
#     # test removing triggers
#     client.remove_trigger('junk', 'insert_ts')
#     # test upsert
#     client.upsert_meta('one', {'order': 1, 'blarg': 1})
#     # test select
#     assert client.select({'order': 1, 'blarg': 1}) == "(<TSDBStatus.OK: 0>, {'one': {}})"

# set_up_server()
# test_client()
