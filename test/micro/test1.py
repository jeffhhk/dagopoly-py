# run as:
#   python -m test.micro.test1

import unittest

import os
import sys
import random
from collections import namedtuple
import heapq
import itertools

from dagopoly.micro.block import *
from dagopoly.micro.exogenous import *
from dagopoly.micro.config import Config
_adir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

Dagopoly().setConf(Config(
        adir=os.path.join(_adir, "storage_test")))

@block("v0.0.0")
def counting():
    yield 1
    yield 2
    yield 3

class TestBlockMethods(unittest.TestCase):

    def test_placebo(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_counting_1(self):
        tmp = counting()
        n = sum(1 for _ in tmp.get())
        self.assertEqual(n,3)

    def test_counting_2(self):
        with self.assertRaises(TypeError):
            sum(1 for _ in counting.get())

    def test_counting_3(self):
        with self.assertRaises(TypeError):
            sum(1 for _ in counting())


if __name__ == '__main__':
    unittest.main()
