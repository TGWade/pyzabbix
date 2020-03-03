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
from pprint import pprint
import json
import yaml
import argparse

# sys.exit(0)

PROJHOME = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, PROJHOME)

from creds import USER, PASSWORD
from zenv import ZSERVERS_URL
from zbxlib import logerror, logdebug

VERBOSE = False
DRYRUN = True
DEBUG = False
DO_ONCE = False

ZABBIX_URL = None
ZABBIX_API_URL = None

headers = {
    'Content-Type': 'application/json-rpc',
}


def zserver_auth():
    ########################################
    # user.login
    ########################################
    auth_payload = {
        "jsonrpc" : "2.0",
        "method" : "user.login",
        "params": {
            'user': USER,
            'password': PASSWORD,
        },
        "auth": None,
        "id": 0,
    }


    res = requests.post(ZABBIX_API_URL, data=json.dumps(auth_payload), headers=headers)
    print( res)
    res = res.json()
    print('user.login response')
    pprint(res)

    return res['result']


def get_hosts():
    ########################################
    # host.get
    ########################################
    payload = {
        "jsonrpc" : "2.0",
        "method" : "host.get",
        "params": {
            'output': [
                'hostid',
                'name'],
        },
        "auth": AUTH,
        "id": 2,
    }
    res2 = requests.post(ZABBIX_API_URL, data=json.dumps(payload), headers=headers)
    res2 = res2.json()
    print('host.get response')
    pprint(res2)


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
    res2 = requests.post(ZABBIX_API_URL, data=json.dumps(payload), headers=headers)
    res2 = res2.json()
    print('host.get response')
    # pprint(res2)
    print(yaml.dump(res2, indent=4))


def get_usergroups():
    payload = {
        "jsonrpc": "2.0",
        "method": "usergroup.get",
        "params": {
            "output": [
                "name",
                "usrgrpid"
            ]
        },
        "auth": AUTH,
        "id": 2,
    }
    res2 = requests.post(ZABBIX_API_URL, data=json.dumps(payload), headers=headers)
    res2 = res2.json()
    print('host.get response')
    # pprint(res2)
    print(yaml.dump(res2, indent=4))
    return res2.get('result')


def get_users(user_group=None):

    payload = {
        "jsonrpc": "2.0",
        "method": "user.get",
        "params": {
            "selectUsrgrps": "extend",
            "output": [
                "alias",
                "userid",
            ]
        },
        "auth": AUTH,
        "id": 2,
    }

    user_group_id = None
    if user_group is not None:
        user_groups = get_usergroups()
        for _ug in user_groups:
            if _ug.get('name') == user_group:
                user_group_id = _ug.get('usrgrpid')
    logdebug("user_group_id: %s" % user_group_id)

    if user_group_id is not None:
        payload['params']['usrgrpids'] = [user_group_id]

    res2 = requests.post(ZABBIX_API_URL, data=json.dumps(payload), headers=headers)
    res2 = res2.json()
    print('host.get response')
    # pprint(res2)
    print(yaml.dump(res2, indent=4))

# TODO : Add for updating user


def update_user(userid, add_user_group_id=None):

    pass


def update_users(user_group=None, add_user_group=None):

    pass


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
    parser.add_argument('--zenv', '-e', action='store', default='prod', required=True)
    parser.add_argument('--usergroup', '--ug', action='store', default=None)
    parser.add_argument('opval', nargs='?', default='templates', choices=op_choices)

    args = parser.parse_args()

    VERBOSE = args.verbose
    DEBUG = args.debug
    DRYRUN = args.dryrun
    DO_ONCE = args.doonce

    ZABBIX_URL = ZSERVERS_URL.get(args.zenv, None)
    logdebug("ZABBIX_URL: %s" % ZABBIX_URL)

    if ZABBIX_URL is None:
        logerror("Zabbix server url cannot be found")
        sys.exit(2)

    ZABBIX_API_URL = ZABBIX_URL + '/api_jsonrpc.php'

    logdebug("ZABBIX_API_URL: %s" % ZABBIX_API_URL)

    AUTH = zserver_auth()

    if args.opval == 'templates':
        get_templates()
    elif args.opval == 'hosts':
        get_hosts()
    elif args.opval == 'usergroups':
        get_usergroups()
    elif args.opval == 'users':
        get_users(args.usergroup)

