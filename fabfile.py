from __future__ import unicode_literals

from fabric.api import cd, local, put, run, task


@task
def pack():
    local('python setup.py sdist --formats=gztar', capture=False)


@task
def deploy():
    dist = local('python setup.py --fullname', capture=True).strip()
    put('dist/%s.tar.gz' % dist, '/tmp/dropapp.tar.gz')
    run('mkdir /tmp/dropapp')
    with cd('/tmp/dropapp'):
        run('tar xzf /tmp/dropapp.tar.gz')
        run('/var/www/dropapp/env/bin/python setup.py install')
    run('rm -rf /tmp/dropapp /tmp/dropapp.tar.gz')
    run('touch /var/www/dropapp.wsgi')


@task
def clean():
    local('python setup.py clean --all')
    local('rm -rf *.pyc build dist dropapp.egg-info')
