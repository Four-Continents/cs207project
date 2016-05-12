#!/usr/bin/env python3
from tsdb import TSDBServer, DictDB
from timeseries import timeseries as ts
from tsdb import *


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

NUMVPS = 5


def main():
    # we augment the schema by adding columns for 5 vantage points
    for i in range(NUMVPS):
        schema["d_vp-{}".format(i)] = {'convert': float, 'index': 1}
    # db = DictDB(schema, 'pk')
    db = connect("/tmp/test2.dbdb", "/tmp/test2_idx.dbdb", schema)
    server = TSDBServer(db, 30000)
    server.run()

if __name__ == '__main__':
    main()
