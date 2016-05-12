import timeseries as ts
from tsdb import *
import time

from tsdb import TSDBClient
import timeseries as ts
import numpy as np
import time
import scipy.stats

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
client = TSDBClient(30000)
client.insert_ts("fifty", ts.TimeSeries([1, 2, 3], [2, 4, 9]))
client.upsert_meta('fifty', {'order': 1, 'blarg': 1})
res = client.select({}, fields=['order', 'ts'], additional={'sort_by': '-order'})
print(res)


# db = connect("/tmp/test2.dbdb", "/tmp/test2_idx.dbdb", schema)
#
# db.insert_ts("two", ts.TimeSeries([1, 2, 3], [2, 4, 9]))
# print(db.select({'order': -1}, fields=['order', 'ts'], additional={'sort_by': '-order'}))
# # # print(db.get("three"))
# # time.sleep(500)
# print(db.select({'order': -1}, fields=['order', 'ts'], additional={''}))
# db.close()

# print("Test one")
# db.set("rahul", "aged1")
# print(db.get("rahul"))
# db.set("pavlos", "aged")
# db.set("rahul", "aged")
# print(db.get("rahul"))
# db.set("kobe", "stillyoung")
# db.close()
# db = connect("/tmp/test2.dbdb")
# try:
#     print(db.get("rahul"))
# except:
#     print("failed like it was supposed to")

# print("Test two")
# db.set("rahul", "aged")
# db.set("pavlos", "aged")
# db.set("kobe", "stillyoung")
# db.commit()
# db.close()
# db = connect("/tmp/test2.dbdb")
# print(db.get("rahul"))

# print("Test three")
# db.set("rahul", "young")
# print(db.get("rahul"))
# db.close()
# db = connect("/tmp/test2.dbdb")
# print(db.get("rahul"))
#
# print("Test four")
# db.set("rahul", "young")
# db.commit()
# db.close()
# db = connect("/tmp/test2.dbdb")
# print(db.get("rahul"))
#
# db.delete("pavlos")
# db.commit()
