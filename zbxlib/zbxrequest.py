import requests
import json
from copy import deepcopy
from .simplelogger import logdebug, write_json

headers = {
    'Content-Type': 'application/json-rpc',
}


class ZBXRequest:

    def __init__(self, auth_tag, api_url, method=None, params=None, verbose=False):
        self.verbose = verbose
        self.method = method
        self.auth_tag = auth_tag
        self.api_url = api_url
        self.params = params
        self.status_code = None
        if self.params is not None:
            self.set_params(params)

    def set_method(self, method):
        self.method = method
        return self

    def set_params(self, params_dict):
        if params_dict is None:
            self.params = None
        else:
            self.params = deepcopy(params_dict)
        return self

    def post(self):
        if self.method is None or self.params is None:
            raise AttributeError("method or params is not set")

        payload = {
            "jsonrpc": "2.0",
            "method": self.method,
            "params": self.params,
            "auth": self.auth_tag,
            "id": 2,
        }
        res2 = requests.post(self.api_url, data=json.dumps(payload), headers=headers)
        self.status_code = res2.status_code
        try:
            res2 = res2.json()
            retval = res2.get('result')
            if self.verbose:
                logdebug('%s.%s: result: \n%s' % (__name__, self.post.__name__, write_json(retval)))
        except Exception as err:
            retval = None
            if self.verbose:
                logdebug('%s.%s: result: \n%s' % (__name__, self.post.__name__, res2))

        return retval
