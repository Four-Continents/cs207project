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

# to run, type in command line: ```PYTHONPATH=. py.test -vv tests/test_tsdb_server.py```
EPS = 1e-6
TEST_PORT = 9500
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
    empty_schema = {
        'pk': {'convert': lambda x: x, 'index': None},
        'ts': {'convert': lambda x: x, 'index': None},
        'order': {'convert': int, 'index': 1},
        'mean': {'convert':float, 'index':1},
        'std': {'convert':float, 'index':1}
    }
    fNames = ['/tmp/four_continents_tsdbs.dbdb', '/tmp/four_continents_tsdbs_idx.dbdb']
    os.remove(fNames[0])
    os.remove(fNames[1])
    db = connect(fNames[0], fNames[1], empty_schema)
    s = TSDBServer(db, TEST_PORT) # Create a server
    t = ServerThread(s)
    t.daemon = True
    t.start()
    return t

def _list_equal(a, b):
    if len(a) != len(b):
        return False
    for i in range(len(a)):
        if a[i] != b[i]:
            return False
    return True

def test_insert(setup):
    # This test looks at some of the core server functions
    # Normally, this would be split over multiple tests, but the server threading makes it
    # more complex to stop the server nicely, resulting in the port not being freed before the next test
    while not setup.running:
        time.sleep(0.01)

    print ('Running...')
    info = {'pk':'ts-1', 'ts':ts.TimeSeries([1, 2, 3, 4, 5], [10, 15, 20, 15, 20])}
    info2 = {'pk':'ts-2', 'ts':ts.TimeSeries([1, 2, 3, 4, 5], [10, 15, 30, 15, 20])}
    client = TSDBClient(TEST_PORT)

    # Test select
    _, res = client.select()

    assert not res

    client.insert_ts( info['pk'], info['ts'])
    client.insert_ts( info2['pk'], info2['ts'])

    _, res = client.select(fields=['ts'])

    # Check primary keys and times/values for the time series
    assert 'ts-1' in res and 'ts-2' in res

    assert _list_equal(res['ts-1']['ts']['values'], info['ts'].values) and _list_equal(res['ts-1']['ts']['times'],
                                                                                       info['ts'].times)
    assert _list_equal(res['ts-2']['ts']['values'], info2['ts'].values) and _list_equal(res['ts-2']['ts']['times'],
                                                                                       info2['ts'].times)


    # Augumented select
    _, res = client.augmented_select('corr', ['dist'], info['ts'])
    # client.augmented_select('corr', ['dist'], query, {'vp': True})
    print (res)

    assert 'ts-1' in res and 'ts-2' in res

    assert (res['ts-2']['dist'] - 0.9601936788280847) < EPS and res['ts-1']['dist'] < EPS

    # Upsert
    client.upsert_meta('ts-1', {'order':10})
    _, res = client.select(fields=['order'])
    assert (res['ts-1']['order'] == 10) and (res['ts-2']['order'] == -1)
    print (res)

    # Check delete works
    client.delete('ts-1')
    _, res = client.select(fields=['ts'])
    assert 'ts-1' not in res and 'ts-2' in res
    assert _list_equal(res['ts-2']['ts']['values'], info2['ts'].values) and _list_equal(res['ts-2']['ts']['times'],
                                                                                       info2['ts'].times)

    # Delete the last element - DB should be empty
    client.delete('ts-2')
    _, res = client.select()

    assert not res

    # print(res)

    # client.populate_db()
    # client.augmented_select('corr', info['ts'])

    # print (t)
    # res = client.select()
    # print(res)
    # client.
    assert 0