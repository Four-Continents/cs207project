from tsdb import tsdb_serialization as ts
import pytest


def mock_serialize():
    a = {'op': 'insert_ts', 'ts': {'values': [1, 4, 9], 'times': [1, 2, 3]}, 'pk': 'one'}
    b = ts.serialize(a)
    return a, b


def test_Deserializer_serialize():
    a, b = mock_serialize()
    deserializer = ts.Deserializer()
    deserializer.append(b)
    if deserializer.ready():
        assert deserializer.deserialize() == a

# test_Deserializer_serialize()
