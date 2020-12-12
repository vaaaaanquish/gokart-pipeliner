from copy import deepcopy

import luigi

from gokart_pipeliner.enum import TYPING

luigi.retcodes.retcode.already_running = 10
luigi.retcodes.retcode.missing_data = 20
luigi.retcodes.retcode.not_run = 30
luigi.retcodes.retcode.task_failed = 40
luigi.retcodes.retcode.scheduling_error = 50


class ConfigManager:
    def __init__(self,
                 params: TYPING.PARAMS = dict(),
                 config_path_list: TYPING.STR_LIST = list()):
        self._init_config(config_path_list)
        self.static_params = params

    def _init_config(self, config_path_list: TYPING.STR_LIST):
        """Add config from config_path_list."""
        luigi.configuration.core.PARSER = 'ini'
        for x in config_path_list:
            assert luigi.configuration.add_config_path(x)

    def make_running_params(self, dynamic_params: TYPING.PARAMS):
        params = deepcopy(self.static_params)
        params.update(dynamic_params)
        return params
