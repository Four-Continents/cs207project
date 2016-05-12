from tsdb import DictDB, TSDBClient, TSDBStatus, TSDBServer
import timeseries as ts
import pytest
import numpy as np

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

EPS = 1e-8

# @pytest.fixture
# def server():
#     # we augment the schema by adding columns for 5 vantage points
#     for i in range(5):
#         schema["d_vp-{}".format(i)] = {'convert': float, 'index': 1}
#     db = DictDB(schema, 'pk')
#     server = TSDBServer(db, 30000)
#     # print(schema)
#
#     return server
#
# def setup_client(client, numTS):
#     from go_client import tsmaker
#
#     # Set up numTS time series
#     mus = np.random.uniform(low=0.0, high=1.0, size=numTS)
#     sigs = np.random.uniform(low=0.05, high=0.4, size=numTS)
#     jits = np.random.uniform(low=0.05, high=0.2, size=numTS)
#
#     # dictionaries for time series and their metadata
#     tsdict = {}
#     metadict = {}
#     for i, m, s, j in zip(range(numTS), mus, sigs, jits):
#         meta, tsrs = tsmaker(m, s, j)
#         # the primary key format is ts-1, ts-2, etc
#         pk = "ts-{}".format(i)
#         tsdict[pk] = tsrs
#         meta['vp'] = False  # augment metadata with a boolean asking if this is a  VP.
#         metadict[pk] = meta
#
#     # choose 5 distinct vantage point time series
#     vpkeys = ["ts-{}".format(i) for i in np.random.choice(range(numTS), size=5, replace=False)]
#     for i in range(5):
#         # add 5 triggers to upsert distances to these vantage points
#         client.add_trigger('corr', 'insert_ts', ["d_vp-{}".format(i)], tsdict[vpkeys[i]])
#         # change the metadata for the vantage points to have meta['vp']=True
#         metadict[vpkeys[i]]['vp'] = True
#     # Having set up the triggers, now insert the time series, and upsert the metadata
#     for k in tsdict:
#         client.insert_ts(k, tsdict[k])
#         time.sleep(1)
#         client.upsert_meta(k, metadict[k])


def test_db_init():
    client = TSDBClient(25000, test=True)
    assert client.port == 25000
    return client

# def test_corr(server):
#     server.run()
#     client = test_db_init()
#     setup_client(client, 10)
#     _, query = tsmaker(0.5, 0.2, 0.1)
#     res = client.augmented_select('corr', ['dist'], query, {'vp': True})
#     server.close()
#     client.close()
#     print (res)

def test_corr_small():
    from procs.corr import proc_main

    ts_l = [10, 22, 26, 4, 18]
    ts_l_x = range(len(ts_l))
    ts_ts = ts.TimeSeries(ts_l_x, ts_l).to_json()
    # print (ts_ts)
    res = proc_main(None, {'ts':ts_ts}, {'times':ts_l_x, 'values':ts_l})
    # print (res)
    assert np.abs(res) < EPS
    # assert 0


# def set_up_server():
#     db = DictDB(schema, 'pk')
#     server = TSDBServer(db, 25000)
#     return server

# does not actually send and receive messages from the server.
# Its just a mock test for now.
def test_client():
    client = test_db_init()
    # test adding triggers
    assert client.add_trigger('junk', 'insert_ts', None, 23) is None
    # test insert
    assert client.insert_ts('one', ts.TimeSeries([1, 2, 3], [1, 4, 9])) is None
    # test removing triggers
    assert client.remove_trigger('junk', 'insert_ts') is None
    # test upsert
    assert client.upsert_meta('one', {'order': 1, 'blarg': 1}) is None
    # test select
    assert client.select({'order': 1, 'blarg': 1}) == (TSDBStatus(0), {})

# set_up_server()
# test_client()
