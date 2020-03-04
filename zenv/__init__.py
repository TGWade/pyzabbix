import sys

try:
    from .local import ZSERVERS_URL, ZABBIXENVS_DICT
except ImportError:
    print("ERROR: no local.py file with ZSERVERS_URL to import, use local.template.py as a template and copy to local.py", sys.stderr)
    raise ImportError

ENV_NAME = None
ZABBIXENV = None

# print(__name__)


class ZabbixEnv:
    def __init__(self, env_name, env_dict):
        setattr(self, 'env_name', env_name)
        for _k, _v in env_dict.items():
            setattr(self, _k, _v)


def set_zabbix_env(env_name, verbose=False):
    global ENV_NAME
    global ZABBIXENV

    if env_name not in ZABBIXENVS_DICT.keys():
        raise AttributeError("%s: env %s not found in ZABBIXENVS_DICT" %  (__name__, env_name))

    ENV_NAME = env_name
    ZABBIXENV = ZabbixEnv(env_name, ZABBIXENVS_DICT.get(env_name))


    return ZABBIXENV


def get_zabbix_env():
    return ZABBIXENV
