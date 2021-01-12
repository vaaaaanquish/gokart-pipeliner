import unittest
from unittest.mock import patch

import gokart

from gokart_pipeliner.instantiation_task import InstantiationTask


class MockGokartTask(gokart.TaskOnKart):
    pass


class MockGokartTargetTask(gokart.TaskOnKart):
    target = gokart.TaskInstanceParameter()


class TestInstantiationTask(unittest.TestCase):
    def _mock_instantiation_tasks(self, mock):
        mock.instantiation_dict_task.side_effect = lambda x, y: {
            k: v()
            for k, v in x.items()
        }
        mock.instantiation_task.side_effect = lambda x, y: x()

    @patch('gokart_pipeliner.InstantiationTask')
    def test_run(self, mock):
        mock = self._mock_instantiation_tasks(mock)
        output = InstantiationTask.run(MockGokartTask)
        self.assertEqual(output, MockGokartTask())

    @patch('gokart_pipeliner.InstantiationTask')
    def test_run_list(self, mock):
        mock = self._mock_instantiation_tasks(mock)
        output = InstantiationTask.run([MockGokartTask, MockGokartTargetTask])
        self.assertEqual(output, MockGokartTargetTask(target=MockGokartTask()))

    @patch('gokart_pipeliner.InstantiationTask')
    def test_run_dict(self, mock):
        mock = self._mock_instantiation_tasks(mock)
        output = InstantiationTask.run({'target': MockGokartTask})
        self.assertDictEqual(output, {'target': MockGokartTask()})

    @patch('gokart_pipeliner.InstantiationTask')
    def test_run_list_dict(self, mock):
        mock = self._mock_instantiation_tasks(mock)
        output = InstantiationTask.run([{
            'target': MockGokartTask
        }, MockGokartTargetTask])
        self.assertEqual(output, MockGokartTargetTask(target=MockGokartTask()))

    @patch('gokart_pipeliner.InstantiationTask')
    def test_instantiation_dict_task(self, mock):
        mock.run.side_effect = lambda x, y: x()
        task = {'foo': MockGokartTask}
        before_task = None
        target = {'foo': MockGokartTask()}

        output = InstantiationTask.instantiation_dict_task(task, before_task)
        self.assertDictEqual(output, target)

    def test_instantiation_task(self):
        task = MockGokartTask
        before_task = None
        output = InstantiationTask.instantiation_task(task, before_task)
        self.assertIsInstance(output, gokart.TaskOnKart)

    def test_instantiation_task_target(self):
        task = MockGokartTargetTask
        before_task = MockGokartTask()
        output = InstantiationTask.instantiation_task(task, before_task)
        self.assertIsInstance(output, gokart.TaskOnKart)

    def test_instantiation_task_dict(self):
        task = MockGokartTargetTask
        before_task = {'target': MockGokartTask()}
        output = InstantiationTask.instantiation_task(task, before_task)
        self.assertIsInstance(output, gokart.TaskOnKart)

    def test_instantiation_task_override_requires(self):
        task = MockGokartTargetTask
        before_task = MockGokartTask()
        task.requires = lambda x: 'foo'
        params = {'MockGokartTargetTask': {'override_requires': False}}
        task = InstantiationTask.instantiation_task(task, before_task, params=params)
        output = task.requires()
        self.assertEqual(output, 'foo')

    def test_override_requires(self):
        task = MockGokartTargetTask
        task = InstantiationTask.override_requires(task, ['target'])
        output = task.requires(task)
        self.assertDictEqual(output, {'target': task.target})

    def test_override_requires_get_input_targets(self):
        task = MockGokartTargetTask
        task.input = lambda: {'target': 'foo'}
        task = InstantiationTask.override_requires(task, ['target'])

        output = task._get_input_targets(task, 'target')
        self.assertEqual(output, 'foo')

        output = task._get_input_targets(task, None)
        self.assertEqual(output, 'foo')
