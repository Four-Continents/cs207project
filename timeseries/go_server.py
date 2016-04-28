#!/usr/bin/env python3
from tsdb import TSDBServer, DictDB
from timeseries import timeseries as ts


def identity(x):
    return x

schema = {
  'pk': {'convert': identity, 'index': None},
  'ts': {'convert': identity, 'index': None},
  'order': {'convert': int, 'index': 1},
  'blarg': {'convert': int, 'index': 1},
  'useless': {'convert': identity, 'index': None},
}


def main():
    db = DictDB(schema)
    # db.insert_ts('one', ts.TimeSeries([1, 2, 3], [1, 4, 9]))
    # db.insert_ts('two', ts.TimeSeries([2, 3, 4], [4, 9, 16]))
    # db.insert_ts('three', ts.TimeSeries([9, 3, 4], [4, 0, 16]))
    # db.insert_ts('four', ts.TimeSeries([0, 0, 4], [1, 0, 4]))
    # db.upsert_meta('one', {'order': 1, 'blarg': 1})
    # db.upsert_meta('two', {'order': 2})
    # db.upsert_meta('three', {'order': 1, 'blarg': 2})
    # db.upsert_meta('four', {'order': 2, 'blarg': 2})
    # print(db.indexes)
    # print(db.rows)
    server = TSDBServer(db, 25000)
    server.run()

if __name__ == '__main__':
    main()
