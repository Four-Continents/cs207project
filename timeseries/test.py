from tsdb import tsdb_error
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
