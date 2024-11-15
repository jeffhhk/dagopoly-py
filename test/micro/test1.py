# run as:
#   python -m test.micro.test1

import unittest

import os
import sys
import random
from collections import namedtuple
import heapq
import itertools

from dagopoly.micro.basics import *
from dagopoly.micro.picklegz import *
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


    # demonstrates: PickleGzIter is not iterable (fixed)
    def test_picklgz_iter(self):
        relf = "test_temp_foo_{}.gz".format(random.randint(0,9000000)+1000000)
        PickleGz.write((str(n) for n in range(10)),relf)
        st = ",".join(PickleGz.read(relf))
        #print("hello {}".format(st))
        if(os.path.exists(relf)):
            os.unlink(relf)

if __name__ == '__main__':
    unittest.main()
