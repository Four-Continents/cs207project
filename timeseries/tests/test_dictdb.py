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
    db.insert_ts("two", ts.TimeSeries([1, 2, 3], [1, 5, 10]))
    assert db.rows["one"]['ts'] == ts.TimeSeries([1, 2, 3], [2, 4, 9])
    # test insert raise error
    with pytest.raises(ValueError):
        db.insert_ts("one", ts.TimeSeries([1, 2, 3], [2, 4, 9]))
    # test upsert
    assert "order" not in list(db.rows["one"].keys())
    assert "blarg" not in list(db.rows["one"].keys())
    db.upsert_meta('one', {'order': 1, 'blarg': 1})
    db.upsert_meta('two', {'order': 2, 'blarg': 2})
    assert db.rows["one"]["order"] == 1
    assert db.rows["one"]["blarg"] == 1
    # test select
    sel_values, field_return = db.select({}, fields=None, additional=None)
    assert len(sel_values) == 2
    assert field_return is None
    sel_values, field_return = db.select({}, fields=[], additional={"sort_by": "+order", "limit": 1})
    assert len(sel_values) == 1
    assert field_return == [{'blarg': 1, 'order': 1, 'pk': 'one'}]
    sel_values, field_return = db.select({}, fields=None, additional={"sort_by": "+order", "limit": 1})
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
    assert db._filter_data("blarg", {'<=': 1}, set(["one"])) == set(["one"])
    # test sorting and limit
    assert db._sort_and_limit(["one", "two"], additional={"sort_by": "-blarg", "limit": 1}) == list(["two"])

test_db_ops()
