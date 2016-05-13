# #  PYTHONPATH=. py.test -vv tests/test_restAPI.py 

from tsdb.tsdb_httpServer import app
import asyncio
import threading
import time
from tsdb.tsdb_server import TSDBServer
from tsdb.dictdb import DictDB, connect
import timeseries as ts
import requests

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


def setup():
	schema = {
	'pk': {'convert': str, 'index': None},  # will be indexed anyways
	'ts': {'convert': str, 'index': None},
	'order': {'convert': int, 'index': 1},
	'blarg': {'convert': int, 'index': 1},
	'useless': {'convert': str, 'index': None},
	'mean': {'convert': float, 'index': 1},
	'std': {'convert': float, 'index': 1},
	'vp': {'convert': bool, 'index': 1}
	}
	db = connect("/tmp/four_continents.dbdb", "/tmp/four_continents_idx.dbdb", schema)
	s = TSDBServer(db, port=30000) # Create a server
	t = ServerThread(s)
	return t

def run_rest_server():
	app.config["JSON_SORT_KEYS"] = False
	app.run(debug=True)
	return app

def test_insert_ts():
    s = setup()
    s.daemon = True
    s.start()

    web = ServerThread(app, True)
    web.daemon = True
    web.start()

  
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
    # s = setup()
    # s.daemon = True
    # s.start()

    # web = ServerThread(app, True)
    # web.daemon = True
    # web.start()

  
    # while not s.running:
    #     time.sleep(0.01)

    # instert ts

    # ts1 = '{"1": {"ts": {"times": [1, 2, 3], "values": [2, 4, 9]}}}'

    # requests.post('http://127.0.0.1:2200/insert', json = ts1)
    # time.sleep(1)
    requests.post('http://127.0.0.1:2200/upsert_meta', json = '{"1": {"order": 1, "blarg": 1}}')
    time.sleep(1)
    requests.post('http://127.0.0.1:2200/upsert_meta', json = '{"2": {"order": 2, "blarg": 2}}')
    time.sleep(1)
    r = requests.get('http://127.0.0.1:2200/select?fields=order', auth=('user', 'pass'))

    assert r.text == '<pre>{\n    "2": {\n        "order": 2\n    },\n    "1": {\n        "order": 1\n    }\n}</pre>' or '<pre>{\n    "1": {\n        "order": 1\n    },\n    "2": {\n        "order": 2\n    }\n}</pre>'

# def test_augmented_select():
#     s = setup()
#     s.daemon = True
#     s.start()

#     web = ServerThread(app, True)
#     web.daemon = True
#     web.start()

  
#     while not s.running:
#         time.sleep(0.01)

#     # instert ts

#     ts1 = '{"1": {"ts": {"times": [1, 2, 3], "values": [2, 4, 9]}}}'

#     # requests.post('http://127.0.0.1:2200/insert', json = ts1)
#     # time.sleep(1)
#     requests.post('http://127.0.0.1:2200/upsert_meta', json = '{"1": {"order": 1, "blarg": 1}}')
#     time.sleep(1)
#     requests.post('http://127.0.0.1:2200/upsert_meta', json = '{"2": {"order": 2, "blarg": 2}}')
#     time.sleep(1)
#     r = requests.get('http://127.0.0.1:2200/select?fields=order', auth=('user', 'pass'))

#     assert r.text == '<pre>{\n    "2": {\n        "order": 2\n    },\n    "1": {\n        "order": 1\n    }\n}</pre>' or '<pre>{\n    "1": {\n        "order": 1\n    },\n    "2": {\n        "order": 2\n    }\n}</pre>'
