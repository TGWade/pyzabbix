
import json
import requests
from pprint import pformat
from zenv import get_zabbix_env

 # from . import MODULE_NAME
from .simplelogger import write_json, logdebug


def zserver_auth(zabbix_api_url=None, user=None, password=None, verbose=False):

    auth_payload = {
        "jsonrpc" : "2.0",
        "method" : "user.login",
        "params": {
            'user': user,
            'password': password,
        },
        "auth": None,
        "id": 0,
    }

    headers = {
        'Content-Type': 'application/json-rpc',
    }

    if verbose:
        logdebug("%s.%s zabbix_api_url: %s" % (__name__, zserver_auth.__name__,
                                               zabbix_api_url))
        logdebug("%s.%s auth_payload: \n%s" % (__name__, zserver_auth.__name__,
                                               write_json(auth_payload)))
        logdebug("%s.%s headers: \n%s" % (__name__, zserver_auth.__name__,
                                          write_json(headers)))

    res = requests.post(zabbix_api_url, data=json.dumps(auth_payload), headers=headers)
    if verbose:
        logdebug("%s.%s result: \n%s" % (__name__, zserver_auth.__name__, pformat(res)))

    res = res.json()
    if verbose:
        logdebug("%s.%s result: \n%s" % (__name__, zserver_auth.__name__, pformat(res)))

    return res['result']

