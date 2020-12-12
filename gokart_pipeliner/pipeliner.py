from typing import List, Dict, Any
from enum import Enum

import luigi

from gokart_pipeliner.instantiation_task import InstantiationTask

luigi.retcodes.retcode.already_running = 10
luigi.retcodes.retcode.missing_data = 20
luigi.retcodes.retcode.not_run = 30
luigi.retcodes.retcode.task_failed = 40
luigi.retcodes.retcode.scheduling_error = 50


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
        task = InstantiationTask.run(tasks)
        luigi.build(
            [task],
            local_scheduler=True,
        )

    def _init_config(self, config_path_list: TYPING.STR_LIST):
        """Add config from config_path_list."""
        luigi.configuration.core.PARSER = 'ini'
        for x in config_path_list:
            assert luigi.configuration.add_config_path(x)
