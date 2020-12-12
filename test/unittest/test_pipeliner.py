import unittest

from gokart_pipeliner import GokartPipeliner
import luigi


class TestGokartPipeliner(unittest.TestCase):
    def test_init(self):
        gp = GokartPipeliner(params={'foo': 'bar'})
        self.assertIsInstance(gp, GokartPipeliner)
        self.assertDictEqual(gp.params, {'foo': 'bar'})

    def test_init_config(self):
        config_path_list = ['test/unittest/sample_config.ini']
        GokartPipeliner(config_path_list=config_path_list)
        output = luigi.configuration.get_config().get('sample', 'foo')
        self.assertEqual(output, 'foo')

    def test_init_config_asserrt(self):
        config_path_list = ['test/unittest/not_found_config.ini']
        with self.assertRaises(AssertionError):
            GokartPipeliner(config_path_list=config_path_list)
