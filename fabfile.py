# -*- coding: utf-8 -*-
"""
Fabric commands of ``django-newproject`` project.
"""
import fileinput
import os
import subprocess
import sys

from fabric import operations as fabric_op
from fabric import utils as fabric_utils


# Default values
# -----------------------------------------------------------------------------
DEFAULTS = {
    'CAPTURE': True,
    'DJANGO_CURRENT_STABLE': '1.2',
    'DJANGO_REPOSITORY_URL': 'http://code.djangoproject.com/svn/django/tags/releases/%s',
    'GAE': False,
}


# Creators
# -----------------------------------------------------------------------------
class ProjectCreator(object):
    """
    A project creator.
    """
    
    def __init__(self, path, capture=None):
        """
        Initializes a ``ProjectCreator`` object.
        """
        self.path = self.normalize_path(path)
        self.capture = capture
        
        if self.capture is None:
            self.capture = DEFAULTS['CAPTURE']

    @property
    def django_repository_url(self):
        """
        Returns Django's repository URL.
        """
        return DEFAULTS['DJANGO_REPOSITORY_URL'] % DEFAULTS['DJANGO_CURRENT_STABLE']
        
    def create(self):
        """
        Creates the project.
        """
        self.check_path()
        self.copy_skeleton()
        self.replace_vars()
        self.setup_virtualenv()
        self.create_settings_local()

    def normalize_path(self, path):
        """
        Returns the project's directory path normalized (no leading slash).
        """
        if path.endswith('/'): 
            return path[:-1]
        return path
    
    def check_path(self):
        """
        Checks the project's directory path.
        """
        if os.path.exists(self.path):
            fabric_utils.abort("Directory '%s' already exists." % self.path)
        head, tail = os.path.split(self.path)
        if not os.path.exists(head):
            fabric_utils.abort("Directory '%s' does not exist." % head)

    def copy_skeleton(self):
        """
        Copies skeleton to the project's directory.
        """
        fabric_op.local('cp -R project %s' % self.path, capture=self.capture)
        
    def replace_vars(self):
        """
        Replaces variables by their values in project files.
        """
        # DJANGO_REPOSITORY_URL in requirements-prod.txt
        f = '%s/requirements-prod.txt' % self.path
        for line in fileinput.input(f, inplace=1):
            print line.replace(
                '{{DJANGO_REPOSITORY_URL}}', 
                self.django_repository_url)
        
    def setup_virtualenv(self):
        """
        Setup the project's virtualenv environment.
        """
        head, tail = os.path.split(self.path)
        fabric_op.local(
            'pip install -E %s -r %s/requirements.txt' % (tail, self.path), 
            capture=self.capture)

    def create_settings_local(self):
        """
        Creates ``settings_local.py`` file.
        """
        fabric_op.local('cd %s' % self.path, capture=self.capture)
        fabric_op.local(
            'mv %s/settings_local.dev.py.sample %s/settings_local.py' % 
            (self.path, self.path), 
            capture=self.capture)
    

class GAEProjectCreator(ProjectCreator):
    """
    A GAE Project creator.
    """
    
    def create(self):
        """
        Creates the project.
        """
        super(GAEProjectCreator, self).create()
        self.add_django_directory()
    
    def copy_skeleton(self):
        """
        Copies skeleton to the project's directory.
        """
        super(GAEProjectCreator, self).copy_skeleton()
        fabric_op.local(
            'cp -f project_gae/* %s' % self.path, 
            capture=self.capture)    

    def add_django_directory(self):
        """
        Adds ``django`` directory to the root.
        """
        fabric_op.local(
            'svn co %s/django %s/libs/django' % 
            (self.django_repository_url, self.path), 
            capture=self.capture)
                
        remove_dirs = (
            'libs/django/bin',
            'libs/django/contrib/admin',
            'libs/django/contrib/admindocs',
            'libs/django/contrib/auth',
            'libs/django/contrib/databrowse',
            'libs/django/contrib/gis',
            'libs/django/test',
        )
        for d in remove_dirs:
            fabric_op.local(
                'rm -rf %s/%s' % (self.path, d), 
                capture=self.capture)


def _create_project(path, capture=None, gae=False):
    """
    Creates the project.
    
    Takes three arguments:
    
        * ``path``: the project path (where to copy the skeleton)
        * ``capture``: enable or disable Fabric capturing the output
        * ``gae``: is a GAE project?
        
    """
    creator_kwargs = {
        'path': path,
        'capture': capture,
    }
    p = ProjectCreator(**creator_kwargs)
    if gae: p = GAEProjectCreator(**creator_kwargs)
    p.create()


# Fabric commands
# -----------------------------------------------------------------------------
def newproject():
    """
    Fabric command creating the new project.
    """
    yesnobool = lambda v: (v == 'yes') or False 
    boolyesno = lambda v: 'yes' if v else 'no'
    
    path = fabric_op.prompt('Project directory path (example: /Users/jdoe/superproject):')
    
    capture = fabric_op.prompt(
        'Capture command output? (yes/no)', 
        default=boolyesno(DEFAULTS['CAPTURE']))
        
    gae = fabric_op.prompt(
        'Is a Google App Engine project? (yes/no)', 
        default=boolyesno(DEFAULTS['GAE']))
    
    _create_project(str(path), yesnobool(capture), yesnobool(gae))
