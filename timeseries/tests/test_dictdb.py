from tsdb import *
import timeseries as ts
import pytest


def identity(x):
    return x

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


def test_db_init():
    db = connect("/tmp/four_continents.dbdb", "/tmp/four_continents_idx.dbdb", schema)
    assert db._schema == schema
    # assert db.pkfield == "pk"
    return db


def test_db_ops():
    db = test_db_init()
    # test insert
    db.insert_ts("one", ts.TimeSeries([1, 2, 3], [2, 4, 9]))
    db.insert_ts("two", ts.TimeSeries([1, 2, 3], [1, 5, 10]))
    assert db._de_stringify(db.get("one"))['ts'] == ts.TimeSeries([1, 2, 3], [2, 4, 9]).to_json()
    db.close()
    with pytest.raises(ValueError):
        db._assert_not_closed()
    # test upsert
    db = test_db_init()
    assert db._de_stringify(db.get("one"))["order"] == -1
    assert db._de_stringify(db.get("one"))["blarg"] == -1
    db.upsert_meta('one', {'order': 1, 'blarg': 1})
    db.upsert_meta('two', {'order': 2, 'blarg': 2})
    assert db._de_stringify(db.get("one"))["order"] == 1
    assert db._de_stringify(db.get("two"))["blarg"] == 2
    db.close()
    # test select
    db = test_db_init()
    sel_values, field_return = db.select(None, fields=None, additional=None)
    assert len(sel_values) == 2
    assert field_return is None
    sel_values, field_return = db.select(None, fields=[], additional={"sort_by": "+order", "limit": 1})
    assert len(sel_values) == 1
    assert field_return == [{'pk': 'one', 'std': -1, 'blarg': 1, 'mean': -1, 'order': 1, 'vp': False, 'useless': 'null'}]
    db.close()
    db = test_db_init()
    sel_values, field_return = db.select(None, fields=None, additional={"sort_by": "+order", "limit": 1})
    assert list(sel_values) == ['one']
    assert field_return is None
    sel_values, field_return = db.select({'blarg': {'<=': 2}}, fields=['blarg'], additional={"sort_by": "-order", "limit": 1})
    assert sel_values == ["two"]
    assert field_return[0] == {"blarg": 2}
    # test select errors
    with pytest.raises(ValueError):
        sel_values, field_return = db.select({}, fields=[], additional={"sort_by": "-order", "lmt": 1})
    with pytest.raises(ValueError):
        sel_values, field_return = db.select({}, fields=[], additional={"sort_by": "-order", "limit": 1, "lmt": 1})
    with pytest.raises(ValueError):
        sel_values, field_return = db.select({}, fields=[], additional={"sort_by": "+pk"})
    # test predicate filter
    assert db._filter_data("blarg", {'<=': 1}) == set(["one"])
    # test sorting and limit
    assert db._sort_and_limit(["one", "two"], additional={"sort_by": "-blarg", "limit": 1}) == list(["two"])
    print("done")

test_db_ops()
