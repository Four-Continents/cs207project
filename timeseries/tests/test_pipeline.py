import os
from pytest import raises
import pype
import timeseries.timeseries as ts


# to run, type in command line: ```PYTHONPATH=. py.test -vv tests/test_pipeline.py```

samples_dir = os.path.join(os.path.dirname(__file__), '../samples')

tso = ts.TimeSeries(list(range(-50, 50)), list(range(100)))

# Now comes the moment of truth. To run a pype program, just build a Pipeline object from a .ppl file, select a
# component to run, and provide it inputs:

# In a test case, we'd like you to create a TimeSeries object for the numbers -50 through 49 at time points 0 through
# 99 and standardize (mean 0, std 1) using the example0.ppl and example1.ppl pipelines. Show us that the resulting
# output has mean 0 and standard deviation 1.


def get_path(filename):
    return os.path.join(samples_dir, filename)


def test_example0():
    filepath = get_path('example0.ppl')

    pipeline = pype.Pipeline(filepath)
    value = pipeline['standardize'].run(tso)

    assert round(value.mean(), 4) == 0
    assert value.std() == 1


def test_example1():
    filepath = get_path('example1.ppl')

    pipeline = pype.Pipeline(filepath)
    value = pipeline['standardize'].run(tso)

    assert round(value.mean(), 4) == 0
    assert value.std() == 1