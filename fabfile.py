import os
from fabric.api import *


def newproject():
    copy_dir = prompt('Copy to (example: /Users/you/Desktop/yourproject): ')
    check_copy_dir(copy_dir)
    copy_skeleton(copy_dir)
    setup_virtualenv(copy_dir)
    rename_settings_local(copy_dir)


def check_copy_dir(copy_dir):
    if os.path.exists(copy_dir):
        abort("Directory '%s' already exists." % copy_dir)
    head, tail = os.path.split(copy_dir)
    if not os.path.exists(head):
        abort("Directory '%s' does not exist. Please, check it again." % head)


def copy_skeleton(copy_dir):
    if copy_dir.endswith('/'): copy_dir = copy_dir[:-1]
    local('cp -R project %s' % copy_dir, capture=False)


def setup_virtualenv(copy_dir):
    if copy_dir.endswith('/'): copy_dir = copy_dir[:-1]
    head, tail = os.path.split(copy_dir)
    local('cd %s' % copy_dir, capture=False)
    local('pip install -E %s -r %s/requirements.txt' % (tail, copy_dir), capture=False)    


def rename_settings_local(copy_dir):
    local('cd %s' % copy_dir, capture=False)
    local('mv %s/settings_local.dev.py.sample %s/settings_local.py' % (copy_dir, copy_dir), capture=False)
