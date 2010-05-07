#!/usr/bin/env python
import os
import sys

from django.core.servers.fastcgi import runfastcgi


_PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_PROJECT_NAME = PROJECT_DIR.split('/')[-1]

sys.path.insert(0, _PROJECT_DIR)
sys.path.insert(0, os.path.dirname(_PROJECT_DIR))

runfastcgi(method='threaded', daemonize='false')
