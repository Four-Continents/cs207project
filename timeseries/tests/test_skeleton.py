#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from timeseries.skeleton import fib, parse_args
import argparse

__author__ = "vinayps"
__copyright__ = "vinayps"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)

# def test_parse_args():
#     assert isinstance(parse_args(["3"]), argparse)

# test_parse_args()
