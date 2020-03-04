import sys

try:
    from .local import USER, PASSWORD
except ImportError:
    print("ERROR: no local.py file with credentials to import, use local.template.py as a template and copy to local.py", sys.stderr)
    raise ImportError
