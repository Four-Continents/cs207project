from tsdb import tsdb_error
from collections import OrderedDict
from timeseries import timeseries as ts
#
# def identity(x):
#     return x
# schema = {
#   'pk': {'convert': identity, 'index': None},
#   'ts': {'convert': identity, 'index': None},
#   'order': {'convert': int, 'index': 1},
#   'blarg': {'convert': int, 'index': 1},
#   'useless': {'convert': identity, 'index': None},
# }
# sel_rows = list(schema.keys())
# for k, v in schema.items():
#     if k == "pk":
#         sel_rows.remove(k)
# print(sel_rows)

print(ts.TimeSeries([1, 2, 3], [1, 4, 9]).to_json())
a = {"a": 1, "b": 2, "c": 3, "d": 4}
b = zip(a.keys(), a.values())
o_a = OrderedDict(sorted(a.items(), key=lambda t: t[1]))
print({k: a[k] for k in ["a", "b"]})
print(o_a)
