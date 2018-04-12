from Utils import Utils

import json


class Config(object):
    config_data = None

    @staticmethod
    def get(key):
        env = Utils.get_env_var('RUNNING_ENV', None)
        file_name = 'config.loada.json'

        if env is not None and len(env) > 0:
            file_name = 'config.%s.json' % env

        if Config.config_data is None:
            with open('locust/%s' % file_name) as data_file:
                Config.config_data = json.load(data_file)
        return Config.config_data[key]
