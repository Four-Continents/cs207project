import asyncio
import threading
import time
from repl import repl
from tsdb.tsdb_client import TSDBClient
from tsdb.tsdb_server import TSDBServer, basic_schema
from tsdb.dictdb import DictDB, connect
import timeseries as ts
import sys
import os

# to run, type in command line: ```PYTHONPATH=. py.test -s -vv tests/test_repl.py```

class ServerThread(threading.Thread):

    def __init__(self, server):
        super(ServerThread, self).__init__()
        self.server = server
        self.running = False

    def run(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.running = True
        self.server.run()
        print('WARNING: server exiting; any client operations after this might hang')


def setup():
    # db = DictDB(basic_schema, 'pk')
    fNames = ['./four_continents_test_repl.dbdb', './four_continents_test_repl_idx.dbdb']
    if os.path.isfile(fNames[0]):
        os.remove(fNames[0])
    if os.path.isfile(fNames[1]):
        os.remove(fNames[1])
    db = connect(fNames[0], fNames[1], basic_schema)
    s = TSDBServer(db) # Create a server
    t = ServerThread(s)
    return t


def test_repl():
    t = setup()
    t.daemon = True
    t.start()

    while not t.running:
        time.sleep(0.01)

    asyncio.set_event_loop(asyncio.new_event_loop())
    client = TSDBClient()
    r = repl.REPL(client)
    output = []

    def print_to_output(*args):
        output.append(' '.join(str(a) for a in args))

    r.print = print_to_output

    def reset():
        del output[:]

    # test do_hello
    r.onecmd('hello')
    assert output == ['Hello!']
    reset()

    # test do_insert with syntax error
    r.onecmd('insert abc @ [4,5,6] into pke')
    r.onecmd('dump')
    assert output == ['Error!']
    reset()

    # test do_insert
    r.onecmd('insert [1,2,3] @ [4, 5, 6] into tabby')
    r.onecmd('dump')
    assert [line.strip() for line in output] == \
           ['OK!', 'tabby', 'ts', 'times :  [4.0, 5.0, 6.0]', 'values :  [1.0, 2.0, 3.0]']
    reset()

    # test do_select
    r.onecmd('select ts')
    assert [line.strip() for line in output] == \
           ['tabby', 'ts', 'times :  [4.0, 5.0, 6.0]', 'values :  [1.0, 2.0, 3.0]']
    reset()

    r.onecmd('select from tabby')
    print([line.strip() for line in output])
    assert [line.strip() for line in output] == \
           ['tabby', 'label :  null', 'order :  -1', 'pk :  tabby']
    reset()

    r.onecmd('select ts, pk')
    assert [line.strip() for line in output] == \
           ['tabby', 'pk :  tabby', 'ts', 'times :  [4.0, 5.0, 6.0]', 'values :  [1.0, 2.0, 3.0]']
    reset()

    r.onecmd('select limit 1')
    assert output == ['Error!']
    reset()

    r.onecmd('select ts limit 1')
    assert [line.strip() for line in output] == \
           ['tabby', 'ts', 'times :  [4.0, 5.0, 6.0]', 'values :  [1.0, 2.0, 3.0]']
    reset()

    r.onecmd('select stats() as mean, std')
    assert [line.strip() for line in output] == \
           ['tabby', 'mean :  2.0', 'std :  0.816496580927726']
    reset()

    r.onecmd('insert [8, 9, 10] @ [11.0, 12.0, 13.0] into calico')
    r.onecmd('select ts order by pk')
    assert [line.strip() for line in output] == \
           ['OK!', 'calico', 'ts', 'times :  [11.0, 12.0, 13.0]', 'values :  [8.0, 9.0, 10.0]', 'tabby', 'ts',
            'times :  [4.0, 5.0, 6.0]', 'values :  [1.0, 2.0, 3.0]']
    reset()

    r.onecmd('select ts order by pk desc')
    assert [line.strip() for line in output] == \
           ['tabby', 'ts', 'times :  [4.0, 5.0, 6.0]', 'values :  [1.0, 2.0, 3.0]', 'calico', 'ts',
            'times :  [11.0, 12.0, 13.0]', 'values :  [8.0, 9.0, 10.0]']
    reset()

    r.onecmd('upsert calico {"label": "cute"}')
    r.onecmd('select label from calico')
    assert [line.strip() for line in output] == ['OK!', 'calico', 'label :  cute']
    reset()