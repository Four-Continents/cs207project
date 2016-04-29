#!/usr/bin/env python3
from tsdb import TSDBServer, DictDB
from timeseries import timeseries as ts


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


def main():
    db = DictDB(schema, 'pk')
    server = TSDBServer(db, 25000)
    server.run()

if __name__ == '__main__':
    main()
