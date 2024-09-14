#!/usr/bin/python3
"""Compress web static package
"""
from fabric.api import env, local, put, run
from datetime import datetime
import os


env.hosts = ['100.25.157.136', '54.237.118.245']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_pack():
    """Function to compress directory
    Return: path to archive on success; None on fail
    """
    # Get current time
    now = datetime.now()
    now = now.strftime('%Y%m%d%H%M%S')
    archive_path = 'versions/web_static_' + now + '.tgz'

    # Create archive
    local('mkdir -p versions')
    result = local('tar -cvzf {} web_static/'.format(archive_path))

    # Check if archiving was successful
    if result.succeeded:
        return archive_path
    return None


def do_deploy(archive_path):
    """distributes an archive to web servers"""
    if not os.path.exists(archive_path):
        return False

    folder = archive_path.split('/')[1].split('.')[0]

    try:
        # Upload the archive to /tmp/
        put(archive_path, '/tmp/')

        # Uncompress the archive
        run('sudo mkdir -p /data/web_static/releases/{}'
            .format(folder))

        run('sudo tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/'
            .format(folder, folder))

        # Remove the archive
        run('sudo rm /tmp/{}.tgz'.format(folder))

        # Create a new the symbolic link
        run('sudo mv /data/web_static/releases/{}/web_static/* \
        /data/web_static/releases/{}'.format(folder, folder))

        run('sudo rm -rf /data/web_static/releases/{}/web_static'
            .format(folder))

        run('sudo rm -rf /data/web_static/current')

        run('sudo ln -s /data/web_static/releases/{}/ \
        /data/web_static/current'.format(folder, folder))

    except Exception as e:
        print('Error:', e)
        return False

    print('New version deployed!')
    return True


def deploy():
    """Creates and distributes an archive to web server"""
    archive_path = do_pack()
    if archive_path is None:
        return False

    return do_deploy(archive_path)
