import sys
import yaml
import json


def log(logstr):
    print(logstr, file=sys.stderr)


def loginfo(logstr):
    log("INFO: %s" % logstr)


def logerror(logstr):
    log("ERROR: %s" % logstr)


def logdebug(logstr):
    log("DEBUG: %s" % logstr)


def logwarn(logstr):
    log("WARNING: %s" % logstr)


def write_yaml(edict, fpath=None, file=None):
    if fpath is None:
        stringout = yaml.dump(edict, indent=4)
        if file is None:
            return stringout
        print("write_yaml: \n%s" % stringout, file=file)
        return
    with open(fpath, 'w') as outfile:
        yaml.dump(edict, outfile, indent=4)


def write_json(edict, fpath=None, dryrun=False):
    # fpath = "%s.json" % fpathroot
    if fpath is None:
        stringout = json.dumps(edict, indent=4)
        return stringout
    if dryrun:
        print("DRYRUN %s \n%s" % (fpathroot, json.dumps(edict, indent=2)))
        return
    with open(fpath, 'w') as outfile:
        json.dump(edict, outfile, indent=2)
