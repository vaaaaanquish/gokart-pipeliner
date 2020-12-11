from typing import List, Dict, Any
from enum import Enum

import gokart
import luigi


class TYPING(Enum):
    PARAMS = Dict[str, Dict[str, Any]]
    STR_LIST = List[str]


class GokartPipeliner:
    def __init__(self,
                 params: TYPING.PARAMS = dict(),
                 config_path_list: TYPING.STR_LIST = list()):
        self._init_config(config_path_list)
        self.params = params

    def run(self,
            tasks: List[luigi.task_register.Register],
            params: TYPING.PARAMS = dict(),
            return_values: TYPING.STR_LIST = list()):
        task = self._instantiation_endpoint_task(tasks)
        luigi.build(
            [task],
            local_scheduler=True,
        )

    def _init_config(self, config_path_list: TYPING.STR_LIST):
        """Add config from config_path_list."""
        luigi.configuration.core.PARSER = 'ini'
        for x in config_path_list:
            assert luigi.configuration.add_config_path(x)

    def _instantiation_endpoint_task(self,
                                     tasks,
                                     before_task=None) -> gokart.TaskOnKart:
        if isinstance(tasks, list):
            for task in tasks:
                if isinstance(task, dict):
                    before_task = self._instantiation_dict_task(
                        task, before_task)
                elif isinstance(task, list):
                    before_task = self._instantiation_endpoint_task(
                        task, before_task)
                else:
                    before_task = self._instantiation_task(task, before_task)

        elif isinstance(tasks, dict):
            before_task = self._instantiation_dict_task(tasks, before_task)
        else:
            before_task = self._instantiation_task(tasks, before_task)

        return before_task

    def _instantiation_dict_task(self, task, before_task):
        return {
            k: self._instantiation_endpoint_task(v, before_task)
            for k, v in task.items()
        }

    def _instantiation_task(self, task, before_task):
        task_parameters = [
            var for var, object_name in vars(task).items()
            if isinstance(object_name, gokart.parameter.TaskInstanceParameter)
        ]

        if isinstance(before_task, dict):
            return task(**{t: before_task[t] for t in task_parameters})
        if before_task is None:
            return task()
        return task(**{task_parameters[0]: before_task})
