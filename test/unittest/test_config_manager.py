import unittest

from gokart_pipeliner.config_manager import ConfigManager
import luigi


class TestConfigManager(unittest.TestCase):
    def test_init_config_file(self):
        config_path_list = ['test/unittest/sample_config.ini']
        ConfigManager(config_path_list=config_path_list)
        output = luigi.configuration.get_config().get('sample', 'foo')
        self.assertEqual(output, 'foo')

    def test_init_config_file_asserrt(self):
        config_path_list = ['test/unittest/not_found_config.ini']
        with self.assertRaises(AssertionError):
            ConfigManager(config_path_list=config_path_list)
