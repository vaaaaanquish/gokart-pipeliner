import os
from copy import deepcopy
from configparser import ConfigParser

import luigi

from gokart_pipeliner.enum import TYPING


class ConfigManager:
    def __init__(self,
                 params: TYPING.PARAMS = dict(),
                 config_path_list: TYPING.STR_LIST = list()):
        self._set_luigi_retcodes()
        self._init_config(config_path_list)
        self._read_environ()
        self.static_params = params

    def _set_luigi_retcodes(self):
        luigi.retcodes.retcode.already_running = 10
        luigi.retcodes.retcode.missing_data = 20
        luigi.retcodes.retcode.not_run = 30
        luigi.retcodes.retcode.task_failed = 40
        luigi.retcodes.retcode.scheduling_error = 50

    def _init_config(self, config_path_list: TYPING.STR_LIST):
        """Add config from config_path_list."""
        luigi.configuration.core.PARSER = 'ini'
        for x in config_path_list:
            assert luigi.configuration.add_config_path(x)

    def _read_environ(self):
        config = luigi.configuration.get_config()
        for key, value in os.environ.items():
            super(ConfigParser, config).set(section=None,
                                            option=key,
                                            value=value.replace('%', '%%'))

    def make_running_params(self, dynamic_params: TYPING.PARAMS):
        params = deepcopy(self.static_params)
        params.update(dynamic_params)
        return params
