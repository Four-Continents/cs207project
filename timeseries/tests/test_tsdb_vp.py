import asyncio
import threading
import time
from repl import repl
from tsdb.tsdb_client import TSDBClient
from tsdb.tsdb_server import TSDBServer
from tsdb.dictdb import DictDB, connect
import timeseries as ts
import os
import pytest

# to run, type in command line: ```PYTHONPATH=. py.test -vv tests/test_tsdb_vp.py```
EPS = 1e-6
TEST_PORT = 9501
class ServerThread(threading.Thread):

    def __init__(self, server):
        super(ServerThread, self).__init__()
        self.server = server
        self.running = False

    def run(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.running = True
        self.server.run()

@pytest.fixture
def setup():
    schema = {
      'pk': {'convert': str, 'index': None},  # will be indexed anyways
      'ts': {'convert': str, 'index': None},
      'order': {'convert': int, 'index': 1},
      'blarg': {'convert': int, 'index': 1},
      'useless': {'convert': str, 'index': None},
      'mean': {'convert': float, 'index': 1},
      'std': {'convert': float, 'index': 1},
      'vp': {'convert': int, 'index': 1}
    }
    NUMVPS = 5
    for i in range(NUMVPS):
        schema["d_vp-{}".format(i)] = {'convert': float, 'index': 1}
    fNames = ['./four_continents_tsdb_vp.dbdb', './four_continents_tsdb_vp_idx.dbdb']
    if os.path.isfile(fNames[0]):
        os.remove(fNames[0])
    if os.path.isfile(fNames[1]):
        os.remove(fNames[1])
    db = connect(fNames[0], fNames[1], schema)
    s = TSDBServer(db, TEST_PORT) # Create a server

    t = ServerThread(s)
    t.daemon = True
    t.start()
    return t

# def _list_equal(a, b):
#     if len(a) != len(b):
#         return False
#     for i in range(len(a)):
#         if a[i] != b[i]:
#             return False
#     return True

def test_insert(setup):
    # This test looks at some of the core server functions
    # Normally, this would be split over multiple tests, but the server threading makes it
    # more complex to stop the server nicely, resulting in the port not being freed before the next test
    while not setup.running:
        time.sleep(0.01)

    client = TSDBClient(TEST_PORT)

    print('Populating DB...')
    client.populate_db()
    print('Looking for similarity...')
    _, q = client._tsmaker(0.5, 0.2, 0.1)
    res = client.find_similar(q, 5)

    print ('Client return vals:', res)

    # assert 0