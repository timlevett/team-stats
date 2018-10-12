from datetime import datetime
import sys
import json

def hours_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%dT%H:%M:%S.%f%z")
    d2 = datetime.strptime(d2, "%Y-%m-%dT%H:%M:%S.%f%z")
    return abs((d2 - d1).total_seconds()/3600)

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def get_settings():
    with open('settings.json') as f:
        return json.load(f)