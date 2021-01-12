import unittest

import gokart

from gokart_pipeliner.pipeliner import GokartPipeliner


class GokartTaskSample(gokart.TaskOnKart):
    def run(self):
        self.dump(['foo', 'bar'])


class TestGokartPipeliner(unittest.TestCase):
    def test_init(self):
        gp = GokartPipeliner()
        self.assertIsInstance(gp, GokartPipeliner)

    def test_run(self):
        gp = GokartPipeliner()
        result = gp.run([GokartTaskSample], return_value=True, verbose=False)
        self.assertListEqual(result, ['foo', 'bar'])
