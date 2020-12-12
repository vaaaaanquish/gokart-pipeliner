from typing import List

import luigi

from gokart_pipeliner.instantiation_task import InstantiationTask
from gokart_pipeliner.enum import TYPING
from gokart_pipeliner.config_manager import ConfigManager


class GokartPipeliner:
    def __init__(self,
                 params: TYPING.PARAMS = dict(),
                 config_path_list: TYPING.STR_LIST = list()):
        self.config = ConfigManager(params, config_path_list)

    def run(self,
            tasks: List[luigi.task_register.Register],
            params: TYPING.PARAMS = dict(),
            return_values: TYPING.STR_LIST = list()):
        params = self.config.make_running_params(params)
        task = InstantiationTask.run(tasks, params=params)
        luigi.build([task], local_scheduler=True)
