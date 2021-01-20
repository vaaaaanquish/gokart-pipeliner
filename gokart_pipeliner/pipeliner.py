from typing import List
import logging
import sys

import luigi
import gokart

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
            return_value: bool = False,
            verbose: bool = True) -> TYPING.RETURN_VALURE:

        if verbose:
            logging.disable(0)
        else:
            logging.disable(sys.maxsize)

        luigi.auto_namespace(scope=__name__)
        luigi.task_register.Register.disable_instance_cache()
        params = self.config.make_running_params(params)
        task = InstantiationTask.run(tasks, params=params)
        luigi.build([task], local_scheduler=True)
        luigi.task_register.Register.clear_instance_cache()

        if return_value:
            output = task.output()
            if type(output) == list:
                return [x.load() for x in output]
            return output.load()
        return None

    def print_dependence_tree(self,
                              tasks: List[luigi.task_register.Register],
                              params: TYPING.PARAMS = dict()):
        params = self.config.make_running_params(params)
        task = InstantiationTask.run(tasks, params=params)
        print('//-----[dependence_tree]------')
        print(gokart.info.make_tree_info(task))
        print('//----------------------------')
