#! /usr/bin/env python3
# vim: set fileencoding=utf8
#
# authenticate with zabbix api server, and retrieve monitored hosts
# specification : https://www.zabbix.com/documentation/1.8/api
#
# $ python zabbix_api.py
import sys
import os
import requests
from pprint import pprint, pformat
import json
import argparse

# sys.exit(0)

PROJHOME = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, PROJHOME)

from creds import USER, PASSWORD
from zenv import ZSERVERS_URL, set_zabbix_env
from zbxlib import logerror, logdebug, zserver_auth, write_yaml, write_json, ZabbixServerAPI


VERBOSE = False
DRYRUN = True
DEBUG = False
DO_ONCE = False

ZABBIX_URL = None
ZABBIX_API_URL = None
SERVER_API = None

headers = {
    'Content-Type': 'application/json-rpc',
}


# def zserver_auth():
#     ########################################
#     # user.login
#     ########################################
#     auth_payload = {
#         "jsonrpc" : "2.0",
#         "method" : "user.login",
#         "params": {
#             'user': USER,
#             'password': PASSWORD,
#         },
#         "auth": None,
#         "id": 0,
#     }
#
#
#     res = requests.post(ZABBIX_API_URL, data=json.dumps(auth_payload), headers=headers)
#     print( res)
#     res = res.json()
#     print('user.login response')
#     pprint(res)
#
#     return res['result']


def get_hosts():
    ########################################
    # host.get
    ########################################
    params = {
        'output': [
            'hostid',
            'name'],
    }
    res2 = SERVER_API.post("host.get", params)
    if VERBOSE:
        logdebug('%s: response: \n%s' % (get_usergroups.__name__, pformat(res2)))
    return res2
    # payload = {
    #     "jsonrpc" : "2.0",
    #     "method" : "host.get",
    #     "params": {
    #         'output': [
    #             'hostid',
    #             'name'],
    #     },
    #     "auth": AUTH,
    #     "id": 2,
    # }
    # res2 = requests.post(ZABBIX_API_URL, data=json.dumps(payload), headers=headers)
    # res2 = res2.json()
    # print('host.get response')
    # pprint(res2)


def get_templates():
    ########################################
    # host.get
    ########################################
    payload = {
        "jsonrpc": "2.0",
        "method": "template.get",
        "params": {
            "output": [
                "name",
                "templateid"
            ]
        },
        "auth": AUTH,
        "id": 2,
    }

    try:
        res2 = requests.post(ZABBIX_API_URL, data=json.dumps(payload), headers=headers)
        res2 = res2.json()
        if VERBOSE:
            logdebug("%s: \n%s" % (get_templates.__name__, write_json(res2)))
    except Exception as err:
        logerror("%s: %s" % (get_templates.__name__, err))
        return None

    return res2.get('result')


def get_usergroups():
    # payload = {
    #     "jsonrpc": "2.0",
    #     "method": "usergroup.get",
    #     "params": {
    #         "output": [
    #             "name",
    #             "usrgrpid"
    #         ]
    #     },
    #     "auth": AUTH,
    #     "id": 2,
    # }

    params = {
        "output": [
            "name",
            "usrgrpid"
        ]
    }
    res2 = SERVER_API.post("usergroup.get", params)
    if VERBOSE:
        logdebug('%s: response: \n%s' % (get_usergroups.__name__, pformat(res2)))
    return res2

    # res2 = requests.post(ZABBIX_API_URL, data=json.dumps(payload), headers=headers)
    # res2 = res2.json()
    # if VERBOSE:
    #     logdebug('%s: response: \n%s' % (get_usergroups.__name__, write_json(res2)))
    #
    # return res2.get('result')


def get_usergroup_id(user_group):
    user_group_id = None
    if user_group is not None:
        user_groups = get_usergroups()
        for _ug in user_groups:
            if _ug.get('name') == user_group:
                user_group_id = _ug.get('usrgrpid')
    if VERBOSE:
        logdebug("%s: %s" % (get_usergroup_id.__name__, user_group_id))
    return user_group_id


def get_users(user_group=None):

    # payload = {
    #     "jsonrpc": "2.0",
    #     "method": "user.get",
    #     "params": {
    #         "selectUsrgrps": "extend",
    #         "output": [
    #             "alias",
    #             "userid",
    #         ]
    #     },
    #     "auth": AUTH,
    #     "id": 2,
    # }

    params = {
        "selectUsrgrps": "extend",
        "output": [
            "alias",
            "userid",
        ]
    }

    user_group_id = None

    if user_group is not None:
        user_group_id = get_usergroup_id(user_group)

    if user_group_id is not None:
        # payload['params']['usrgrpids'] = [user_group_id]
        params['usrgrpids'] = [user_group_id]

    res2 = SERVER_API.post("user.get", params)
    if VERBOSE:
        logdebug('%s: response: \n%s' % (get_users.__name__, pformat(res2)))
    return res2
    # res2 = requests.post(ZABBIX_API_URL, data=json.dumps(payload), headers=headers)
    # res2 = res2.json()
    # if VERBOSE:
    #     logdebug('%s: response: \n%s' % (get_users.__name__, res2))
    # return res2['result']

# TODO : Add for updating user


def update_user(userid, add_user_group_id=None):

    pass


def update_users(user_group=None, add_user_group=None):

    pass


def test(args):
    params = {
        "selectUsrgrps": "extend",
        "output": [
            "alias",
            "userid",
        ]
    }

    users = SERVER_API.post("user.get", params)
    # logdebug(get_usergroup_id(args.usergroup))

    write_json(users, file=sys.stdout)


if __name__ == '__main__':

    op_choices = [
        'templates',
        'hosts',
        'usergroups',
        'users',
    ]
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action="store_true", default=VERBOSE)
    parser.add_argument('--debug', action="store_true", default=DEBUG)
    parser.add_argument('--dryrun', action="store_true", default=DRYRUN)
    parser.add_argument('--doonce', action='store_true', help="create only one service (for testing)", default=False)
    parser.add_argument('--doit', action="store_true", default=DO_ONCE)
    parser.add_argument('--test', '-t', action="store_true", default=False)
    parser.add_argument('--zenv', '-e', action='store', default='prod', required=True)
    parser.add_argument('--usergroup', '--ug', action='store', default=None)
    parser.add_argument('opval', nargs='?', default='templates', choices=op_choices)

    args = parser.parse_args()

    VERBOSE = args.verbose
    DEBUG = args.debug
    DRYRUN = args.dryrun
    DO_ONCE = args.doonce

    SERVER_API = ZabbixServerAPI(args.zenv, verbose=VERBOSE)

    # ZABBIX_URL = ZSERVERS_URL.get(args.zenv, None)
    ZABBIX_URL = SERVER_API.get_base_url()

    if VERBOSE:
        logdebug("ZABBIX_URL: %s" % ZABBIX_URL)

    if ZABBIX_URL is None:
        logerror("Zabbix server url cannot be found")
        sys.exit(2)

    # ZABBIX_API_URL = ZABBIX_URL + '/api_jsonrpc.php'
    ZABBIX_API_URL = SERVER_API.get_api_url()

    if VERBOSE:
        logdebug("ZABBIX_API_URL: %s" % ZABBIX_API_URL)

    # AUTH = zserver_auth(ZABBIX_API_URL, USER, PASSWORD, verbose=VERBOSE)
    AUTH = SERVER_API.auth(USER, PASSWORD)

    if VERBOSE:
        logdebug("SERVER_API: %s" % pformat(SERVER_API.__dict__))

    # AUTH = zserver_auth_prev()

    if args.test:
        test(args)

    elif args.opval == 'templates':
        write_json(get_templates(), file=sys.stdout)

    elif args.opval == 'hosts':
        write_json(get_hosts(), file=sys.stdout)

    elif args.opval == 'usergroups':
        write_json(get_usergroups(), file=sys.stdout)

    elif args.opval == 'users':
        write_json(get_users(args.usergroup),file=sys.stdout)

