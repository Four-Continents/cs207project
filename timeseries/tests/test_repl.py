import asyncio
import threading
import time
from repl import repl
from tsdb.tsdb_client import TSDBClient
from tsdb.tsdb_server import TSDBServer
from tsdb.dictdb import DictDB
import timeseries as ts


# to run, type in command line: ```PYTHONPATH=. py.test -vv tests/test_repl.py```

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
    empty_schema = {
        'pk': {'convert': lambda x: x, 'index': None},
        'ts': {'convert': lambda x: x, 'index': None},
    }
    db = DictDB(empty_schema, 'pk')
    s = TSDBServer(db) # Create a server
    t = ServerThread(s)
    return t


def test_whatever():
    t = setup()
    t.daemon = True
    t.start()

    while not t.running:
        time.sleep(0.01)

    client = TSDBClient()
    r = repl.DumbREPL(client)
    output = []
    def print_to_output(s):
        output.append(s)
    r.print = print_to_output

    r.onecmd('hello')
    assert output == ['Hello!']
