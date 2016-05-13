from tsdb.tsdb_httpServer import app
import asyncio
import threading
import time
from tsdb.tsdb_server import TSDBServer
from tsdb.dictdb import DictDB, connect
import timeseries as ts
import requests
import pytest
import json
import io, os
import numpy as np

port = 9600
EPS = 1e-6

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
            self.server.run(port=port)
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

    fNames = ['./four_continents_tsdb_rest.dbdb', './four_continents_tsdb_rest_idx.dbdb']
    if os.path.isfile(fNames[0]):
        os.remove(fNames[0])
    if os.path.isfile(fNames[1]):
        os.remove(fNames[1])
    db = connect(fNames[0], fNames[1], schema)
    s = TSDBServer(db, port=30000) # Create a server
    t = ServerThread(s)
    t.daemon = True
    t.start()
    return t

@pytest.fixture
def web():
    # app.config["JSON_SORT_KEYS"] = False
    # app.run(debug=True)
    web = ServerThread(app, True)
    web.daemon = True
    web.start()
    return web

def test_insert_ts(setup, web):

    while not setup.running or not web.running:
        time.sleep(0.01)

    # instert ts
    ts1 = '{"1": {"ts": {"times": [1, 2, 3], "values": [2, 4, 9]}}}'
    ts2 = '{"2": {"ts": {"times": [1, 2, 3], "values": [1, 5, 10]}}}'

    time.sleep(1)
    requests.post('http://127.0.0.1:{}/insert'.format(port), json = ts1)
    time.sleep(1)
    requests.post('http://127.0.0.1:{}/insert'.format(port), json = ts2)
    time.sleep(1)
    r = requests.get('http://127.0.0.1:{}/select'.format(port), auth=('user', 'pass'))

    time.sleep(1)
    # r.text
    assert r.text == '{\n    "1": {},\n    "2": {}\n}' or r.text == '{\n    "2": {},\n    "1": {}\n}'
    # assert r.json() == {'1': {}, '2': {}}

# def test_upsert_md(setup, web):

    requests.post('http://127.0.0.1:{}/upsert_meta'.format(port), json = '{"1": {"order": 1, "blarg": 1}}')
    time.sleep(1)
    requests.post('http://127.0.0.1:{}/upsert_meta'.format(port), json = '{"2": {"order": 2, "blarg": 2}}')
    time.sleep(1)
    r = requests.get('http://127.0.0.1:{}/select?fields=order'.format(port), auth=('user', 'pass'))

    assert r.text == '{\n    "2": {\n        "order": 2\n    },\n    "1": {\n        "order": 1\n    }\n}' or '{\n    "1": {\n        "order": 1\n    },\n    "2": {\n        "order": 2\n    }\n}'
    time.sleep(2)
# def test_augmented_select():

    augmented_data = '{"additional": {"limit": 2, "sort_by": "+order"}, "target": ["damean", "dastd"], "md": {"blarg": {">=": 1}}, "proc": "stats"}'
    r = requests.post('http://127.0.0.1:{}/augmented_select'.format(port), json = augmented_data)
    time.sleep(2)

    res = json.loads(r.text)
    assert '1' in res and '2' in res
    assert res['1']['damean'] - 5.0 < EPS and res['2']['damean'] - 5.333333333333333 < EPS
    assert res['1']['dastd'] - 2.943920288775949 < EPS and res['2']['dastd'] - 3.6817870057290873 < EPS

   # assert r.text == '{\n    "1": {\n        "damean": 5.0,\n        "dastd": 2.943920288775949\n    },\n    "2": {\n        "damean": 5.333333333333333,\n        "dastd": 3.6817870057290873\n    }\n}' or



# def test_delete(setup, web):
    requests.post('http://127.0.0.1:{}/delete'.format(port), json = '2')
    time.sleep(1)
    requests.post('http://127.0.0.1:{}/delete'.format(port), json = '1')
    time.sleep(1)

    r = requests.get('http://127.0.0.1:{}/select'.format(port), auth=('user', 'pass'))

    assert r.text == '{}'

    # def test_find_similar(setup, web):

    # values = np.random.randint(1,100,100)
    # times = np.arange(1,101)
    # k_nearest = 3
    #
    # ts = json.dumps(dict(times = times.tolist(), values = values.tolist(), k_nearest = k_nearest, numElem = 10,
    #                      numVp = 5  ))
    #
    # # ts = '{"times": {}, "values": {}, "k_nearest":{}, "numElem": 10, "numVp": 5}'.format(str(times),
    # #                                                                                       str(values), k_nearest)
    #
    # print ('ts:', ts)
    # # ts_a = io.StringIO()
    # # json.dump( ts, fp=ts_a)
    #
    # r = requests.post('http://127.0.0.1:{}/find_similar'.format(port), json = ts)
    # assert len(json.loads(r.text)) == k_nearest