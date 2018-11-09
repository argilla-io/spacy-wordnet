#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from spacy_wordnet.skeleton import fib

__author__ = "Francisco Aranda"
__copyright__ = "Francisco Aranda"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
