import unittest
from timeseries.procs import stats
import numpy as np


def test_main():
    loop = asyncio.get_event_loop()
    b = ts.TimeSeries([1, 1.5, 2, 2.5, 10], [1, 1, 1, 1, 1]).to_json()
    coro = asyncio.ensure_future(stats.main("ts-one", {'ts': b}, []))
    loop.run_until_complete(coro)
    assert coro.result() == [1.0, 0]

