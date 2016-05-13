from tsdb import Storage
import timeseries as ts
import pytest
import numpy as np

schema = {
    'pk': {'convert': str, 'index': 1},  # will be indexed anyways
    'ts': {'convert': str, 'index': None},
    'order': {'convert': int, 'index': 1},
    'blarg': {'convert': int, 'index': 1},
    'useless': {'convert': str, 'index': None},
    'mean': {'convert': float, 'index': 1},
    'std': {'convert': float, 'index': 1},
    'vp': {'convert': int, 'index': 1}
}


