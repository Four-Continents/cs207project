# import multiprocessing
# import time
# from tsdb import *
# from tsdb import TSDBServer, DictDB, connect

from tsdb.tsdb_httpServer import app

# #  PYTHONPATH=. py.test -vv tests/test_restAPI.py 



# def run_server():
# 	schema = {
#   'pk': {'convert': str, 'index': None},  # will be indexed anyways
#   'ts': {'convert': str, 'index': None},
#   'order': {'convert': int, 'index': 1},
#   'blarg': {'convert': int, 'index': 1},
#   'useless': {'convert': str, 'index': None},
#   'mean': {'convert': float, 'index': 1},
#   'std': {'convert': float, 'index': 1},
#   'vp': {'convert': bool, 'index': 1}}

# 	NUMVPS = 5
# 	# we augment the schema by adding columns for 5 vantage points
# 	for i in range(NUMVPS):
# 	    schema["d_vp-{}".format(i)] = {'convert': float, 'index': 1}
# 	# db = DictDB(schema, 'pk')
# 	db = connect("/tmp/four_continents.dbdb", "/tmp/four_continents_idx.dbdb", schema)
# 	server = TSDBServer(db, 32360)
# 	server.run()


# def run_rest_server():
# 	app.config["JSON_SORT_KEYS"] = False
# 	app.run(debug=True, port=8889)


# def run_server_process():
# 	server_process = multiprocessing.Process(target=run_server)
# 	server_process.daemon = True
# 	server_process.run()

# 	# rest_server_process = multiprocessing.Process(target=run_rest_server)
# 	# rest_server_process.run()

# 	time.sleep(3)
# 	return server_process #, rest_server_process

# def test_servers():

# 	a = run_server_process()
# 	print("HERE", a)
# 	# b.terminate()
# 	print("Closing server process")
# 	# a.join()
# 	# print("Closing rest server process")
# 	# b.join()

import asyncio
import threading
import time
from tsdb.tsdb_server import TSDBServer
from tsdb.dictdb import DictDB, connect
import timeseries as ts


# to run, type in command line: ```PYTHONPATH=. py.test -vv tests/test_restAPI.py```

class ServerThread(threading.Thread):

    def __init__(self, server):
        super(ServerThread, self).__init__()
        self.server = server
        self.running = False

    def run(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.running = True
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
	s = TSDBServer(db) # Create a server
	t = ServerThread(s)
	return t

def run_rest_server():
	app.config["JSON_SORT_KEYS"] = False
	app.run(debug=True, port=2000)
	return app

def test_whatever():
    s = setup()
    s.daemon = True
    s.start()

    # server_process = threading.Thread(target=run_rest_server)
    # server_process.run()
    run_rest_server()
    print ('Hola')
    app.terminate()



    while not s.running:
        time.sleep(0.01)

    