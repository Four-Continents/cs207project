from tsdb import DictDB
import timeseries as ts
import pytest


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


def test_db_init():
    db = DictDB(schema, 'pk')
    assert db.schema == schema
    assert db.pkfield == "pk"
    return db


def test_db_ops():
    db = test_db_init()
    # test insert
    db.insert_ts("one", ts.TimeSeries([1, 2, 3], [2, 4, 9]))
    assert db.rows["one"]['ts'] == ts.TimeSeries([1, 2, 3], [2, 4, 9])
    # test upsert
    assert "order" not in list(db.rows["one"].keys())
    assert "blarg" not in list(db.rows["one"].keys())
    db.upsert_meta('one', {'order': 1, 'blarg': 1})
    assert db.rows["one"]["order"] == 1
    assert db.rows["one"]["blarg"] == 1
    # test select
    sel_values, field_return = db.select({'blarg': {'<=': 2}}, fields=['blarg'])
    assert sel_values == ["one"]
    assert field_return[0] == {"blarg": 1}
    # test predicate filter
    assert db._filter_data("blarg", {'<=': 2}, set(["one"])) == set(["one"])

# test_db_ops()
