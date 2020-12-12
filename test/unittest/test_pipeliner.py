import unittest

from gokart_pipeliner.pipeliner import GokartPipeliner


class TestGokartPipeliner(unittest.TestCase):
    def test_init(self):
        gp = GokartPipeliner()
        self.assertIsInstance(gp, GokartPipeliner)
