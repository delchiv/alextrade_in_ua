# coding: utf-8

from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run, sudo
import random

REPO_URL = 'https://github.com/delchiv/alextrade_in_ua.git'
PROJECT_NAME = 'alextrade_in_ua'

def deploy():
    site_folder = '/home/%s/sites/%s' % (env.user, env.host)
    source_folder = site_folder + '/src'
    settings_folder = source_folder + '/' + PROJECT_NAME
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(settings_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)
    _restart_apps(env.host)

def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('db', 'static', 'media', 'venv', 'src', 'log'):
        run('mkdir -p %s/%s' % (site_folder, subfolder))

def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'): 
        run('cd %s && git fetch' % (source_folder,))  
    else:
        run('git clone %s %s' % (REPO_URL, source_folder))  
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run('cd %s && git reset --hard %s' % (source_folder, current_commit))

def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../venv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run('virtualenv --python=python2 %s' % (virtualenv_folder,))
    run('%s/bin/pip install -r %s/requirements.txt' % (
            virtualenv_folder, source_folder
    ))

def _update_settings(settings_folder, site_name):
    settings_path = settings_folder + '/settings.py'
    if not exists(settings_path):
        run('cp %s.template %s' % (settings_path, settings_path,))
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        sed(settings_path, "\[PROJECTNAME\]", PROJECT_NAME)
        sed(settings_path, "\[SECRET KEY HERE\]", key)
        sed(settings_path, "\[ALLOWED HOSTS HERE\]", site_name)
        sed(settings_path, "DEBUG = True", "DEBUG = False")

def _update_static_files(source_folder):
    run('cd %s && ../venv/bin/python manage.py collectstatic --noinput' % (source_folder, ))

def _update_database(source_folder):
    run('cd %s && ../venv/bin/python manage.py syncdb' % (source_folder, ))
    run('cd %s && ../venv/bin/python manage.py migrate' % (source_folder, ))

def _restart_apps(site_name):
    sudo('service nginx restart')
    sudo("if initctl status %s | grep -c -q 'start'; then sudo stop %s; fi" % (site_name, site_name,))
    sudo('start %s' % (site_name,))


