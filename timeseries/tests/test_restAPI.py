# #  PYTHONPATH=. py.test -vv tests/test_restAPI.py 

from tsdb.tsdb_httpServer import app
import asyncio
import threading
import time
from tsdb.tsdb_server import TSDBServer
from tsdb.dictdb import DictDB, connect
import timeseries as ts
import requests
import numpy as np
import io
import json
import pytest

Port = 2200

class ServerThread(threading.Thread):

    def __init__(self, server, web=False):
        super(ServerThread, self).__init__()
        self.server = server
        self.running = False
        self.web = web

    def run(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.running = True
        if self.web:
            self.server.run(port=Port)
        else:
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
    db = connect("/tmp/four_continents.dbdb", "/tmp/four_continents_idx.dbdb", schema)
    s = TSDBServer(db, port=30000) # Create a server
    t = ServerThread(s)
    t.daemon = True
    t.start()
    return t

@pytest.fixture
def web():
    app.config["JSON_SORT_KEYS"] = False
    app.run(debug=True)
    web = ServerThread(app, True)
    web.daemon = True
    web.start()
    return web

def test_insert_ts(setup, web):
     
    while not s.running:
        time.sleep(0.01)

    # instert ts
    ts1 = '{"1": {"ts": {"times": [1, 2, 3], "values": [2, 4, 9]}}}'
    ts2 = '{"2": {"ts": {"times": [1, 2, 3], "values": [1, 5, 10]}}}'

    requests.post('http://127.0.0.1:2200/insert', json = ts1)
    time.sleep(1)
    requests.post('http://127.0.0.1:2200/insert', json = ts2)
    time.sleep(1)
    r = requests.get('http://127.0.0.1:2200/select', auth=('user', 'pass'))
    
    time.sleep(1)
    # r.text
    assert r.text == '<pre>{\n    "1": {},\n    "2": {}\n}</pre>' or r.text == '<pre>{\n    "2": {},\n    "1": {}\n}</pre>'
    # assert r.json() == {'1': {}, '2': {}}

def test_upsert_md():
 
    requests.post('http://127.0.0.1:2200/upsert_meta', json = '{"1": {"order": 1, "blarg": 1}}')
    time.sleep(1)
    requests.post('http://127.0.0.1:2200/upsert_meta', json = '{"2": {"order": 2, "blarg": 2}}')
    time.sleep(1)
    r = requests.get('http://127.0.0.1:2200/select?fields=order', auth=('user', 'pass'))

    assert r.text == '<pre>{\n    "2": {\n        "order": 2\n    },\n    "1": {\n        "order": 1\n    }\n}</pre>' or '<pre>{\n    "1": {\n        "order": 1\n    },\n    "2": {\n        "order": 2\n    }\n}</pre>'

# def test_augmented_select():
   
#    augmented_data = '{"additional": {"limit": 2, "sort_by": "+order"}, "target": ["damean", "dastd"], "md": {"blarg": {">=": 1}}, "proc": "stats"}'
#    r = requests.post('http://127.0.0.1:2200/augmented_select', json = augmented_data)
#    time.sleep(2)

#    assert r.text == '{\n    "1": {\n        "damean": 5.0,\n        "dastd": 2.943920288775949\n    },\n    "2": {\n        "damean": 5.333333333333333,\n        "dastd": 3.6817870057290873\n    }\n}' 

def test_delete():
   
   requests.post('http://127.0.0.1:2200/delete', json = '2')
   time.sleep(1)

   requests.post('http://127.0.0.1:2200/delete', json = '1')
   time.sleep(1)

   r = requests.get('http://127.0.0.1:2200/select', auth=('user', 'pass'))

   assert r.text == '<pre>{}</pre>'

def test_find_similar():

    values = np.random.randint(1,100,100)
    times = np.arange(1,101)
    k_nearest = 3

    ts =  {'times': times.tolist(), 'values': values.tolist(), 'k_nearest':k_nearest}

    ts_a = io.StringIO()
    json.dump( ts, fp=ts_a)

    r = requests.post('http://127.0.0.1:2200/find_similar', json = ts_a.getvalue())
    assert len(json.loads(r.text)) == k_nearest
