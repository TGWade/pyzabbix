from pprint import pformat

MODULE_NAME = 'zbxlib'

from .simplelogger import log, loginfo, logerror, logdebug, logwarn, write_yaml, write_json
from .auth import zserver_auth
from .zbxrequest import ZBXRequest

from zenv import set_zabbix_env


ZABBIX_URL = None
ZABBIX_API_URL = None
VERBOSE = False


def set_server_url(server_url):
    global ZABBIX_API_URL
    global ZABBIX_URL

    ZABBIX_URL = server_url
    ZABBIX_API_URL = ZABBIX_URL + '/api_jsonrpc.php'


def get_api_url():
    return ZABBIX_API_URL


class ZabbixServerAPI:

    def __init__(self, env_name, user=None, password=None, verbose=VERBOSE):
        self.verbose = verbose
        self.env_name = env_name
        self.env = set_zabbix_env(env_name, verbose=verbose)
        if verbose:
            logdebug("%s.%s: env \n%s" % (__name__, ZabbixServerAPI.__name__, self.env.__dict__))
        self.auth_tag = None
        self.zbxrequest = None
        self.user = user
        self.password = password
        self.method = None
        self.params = None

    def auth(self, user=None, password=None):
        if user is not None:
            self.user = user
        if password is not None:
            self.password = password

        if self.user is None or self.password is None:
            raise AttributeError("user or password is not set")

        self.auth_tag = zserver_auth(self.get_api_url(),
                                     user=self.user, password=self.password, verbose=self.verbose)
        return self.auth_tag

    def get_base_url(self):
        return self.env.url

    def get_api_url(self):
        return self.get_base_url() + '/api_jsonrpc.php'

    def get_zbxrequest(self):
        if self.zbxrequest is None:
            self.zbxrequest = ZBXRequest(self.auth_tag, self.get_api_url(),
                                         method=self.method, params=self.params,
                                         verbose=self.verbose)
        return self.zbxrequest

    def post(self, method, params):
        self.method = method
        self.params = params
        req = self.get_zbxrequest()
        req.set_method(self.method)
        req.set_params(self.params)

        return req.post()

