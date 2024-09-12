#!/usr/bin/python3
"""distributes an archive to web servers"""

from fabric.api import env, put, run
import os

env.hosts = ['100.25.157.136', '54.237.118.245']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """Deploy a new releas to the server"""

    # Check if the archive file exists
    if not os.path.exists(archive_path):
        return False

    archive = archive_path.split('/')[1].split('.')[0]

    try:
        # Upload the archive to the server
        put(archive_path, '/tmp/')

        #Uncompress the archive
        run('sudo mkdir -p /data/web_static/releases/{}'.format(archive))
        run('sudo tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/'
            .format(archive, archive))

        # Delete the archive from the web server
        run('sudo rm -rf /tmp/{}.tgz'.format(archive))

        # Move the static files to the version file
        run('sudo mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/'
            .format(archive, archive))
        run('sudo rm -rf /data/web_static/releases/{}/web_static'.format(archive))

        # Delete the old symbolic link from the server
        run('sudo rm -rf /data/web_static/current')

        # Create a new symbolic link
        run('sudo ln -sf /data/web_static/releases/{}/ /data/web_static/current'
            .format(archive))

    except Exception as e:
        print(e)
        return False

    print('New version deployed!')
    return True
