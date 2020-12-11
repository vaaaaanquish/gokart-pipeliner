import unittest
from unittest.mock import patch

from gokart_pipeliner import GokartPipeliner
import luigi
import gokart


class MockGokartTask(gokart.TaskOnKart):
    pass


class MockGokartTargetTask(gokart.TaskOnKart):
    target = gokart.TaskInstanceParameter()


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

    @patch('gokart_pipeliner.GokartPipeliner')
    def test_instantiation_endpoint_task(self, mock):
        mock = self._mock_instantiation_endpoint_task(mock)
        output = GokartPipeliner()._instantiation_endpoint_task(MockGokartTask)
        self.assertEqual(output, MockGokartTask())

    @patch('gokart_pipeliner.GokartPipeliner')
    def test_instantiation_endpoint_task_list(self, mock):
        mock = self._mock_instantiation_endpoint_task(mock)
        output = GokartPipeliner()._instantiation_endpoint_task(
            [MockGokartTask, MockGokartTargetTask])
        self.assertEqual(output, MockGokartTargetTask(target=MockGokartTask()))

    @patch('gokart_pipeliner.GokartPipeliner')
    def test_instantiation_endpoint_task_list_dict(self, mock):
        mock = self._mock_instantiation_endpoint_task(mock)
        output = GokartPipeliner()._instantiation_endpoint_task([{
            'target':
            MockGokartTask
        }, MockGokartTargetTask])
        self.assertEqual(output, MockGokartTargetTask(target=MockGokartTask()))

    @patch('gokart_pipeliner.GokartPipeliner')
    def test_instantiation_endpoint_task_dict(self, mock):
        mock = self._mock_instantiation_endpoint_task(mock)
        output = GokartPipeliner()._instantiation_endpoint_task(
            {'target': MockGokartTask})
        self.assertDictEqual(output, {'target': MockGokartTask()})

    @patch('gokart_pipeliner.GokartPipeliner')
    def test_instantiation_dict_task(self, mock):
        mock._instantiation_endpoint_task.side_effect = lambda x, y: x()
        task = {'foo': MockGokartTask}
        before_task = None
        target = {'foo': MockGokartTask()}

        output = GokartPipeliner()._instantiation_dict_task(task, before_task)
        self.assertDictEqual(output, target)

    def test_instantiation_task(self):
        task = MockGokartTask
        before_task = None
        output = GokartPipeliner()._instantiation_task(task, before_task)
        self.assertIsInstance(output, gokart.TaskOnKart)

    def test_instantiation_task_target(self):
        task = MockGokartTargetTask
        before_task = MockGokartTask()
        output = GokartPipeliner()._instantiation_task(task, before_task)
        self.assertIsInstance(output, gokart.TaskOnKart)

    def test_instantiation_task_dict(self):
        task = MockGokartTargetTask
        before_task = {'target': MockGokartTask()}
        output = GokartPipeliner()._instantiation_task(task, before_task)
        self.assertIsInstance(output, gokart.TaskOnKart)

    def _mock_instantiation_endpoint_task(self, mock):
        mock._instantiation_dict_task.side_effect = lambda x, y: {
            k: v()
            for k, v in x.items()
        }
        mock._instantiation_task.side_effect = lambda x, y: x()
