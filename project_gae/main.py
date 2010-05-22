#!/usr/bin/env python
import os
import sys

from google.appengine.ext.webapp import util


# Some shortcuts
ROOT = os.path.dirname(os.path.realpath(__file__))
LIBS = os.path.join(ROOT, 'libs')

# Remove the standard version of Django
for k in [k for k in sys.modules if k.startswith('django')]:
    del sys.modules[k]

# Force sys.path to have our own directory first
sys.path.insert(0, LIBS)

# Must set this env var *before* importing any part of Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


from django.core.management import setup_environ
from django.core.handlers import wsgi

try:
    import settings_local as settings
except ImportError:
    import sys
    sys.stderr.write(
        "Error: tried importing 'settings_local.py' and 'settings.py' "
        "but neither could be found (or they are throwing an ImportError). "
        "Please, come back and try again later.")
    raise

setup_environ(settings)


def main():
    application = wsgi.WSGIHandler()
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
