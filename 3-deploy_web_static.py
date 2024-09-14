#!/usr/bin/python3
"""Compress and deploy web static package."""
from fabric.api import env, local, put, run
from datetime import datetime
import os

# Define the hosts, user, and key file globally
env.hosts = ['100.25.157.136', '54.237.118.245']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_pack():
    """Create a tar archive of the web_static directory.
    Returns:
        str: Path to the created archive on success.
        None: If the archive creation fails.
    """
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    archive_path = f'versions/web_static_{now}.tgz'

    try:
        # Create the versions directory if it does not exist
        local('mkdir -p versions')

        # Create the tar archive
        result = local(f'tar -cvzf {archive_path} web_static/', capture=True)
        if result.succeeded:
            return archive_path
    except Exception as e:
        print(f'Error creating archive: {e}')

    return None


def do_deploy(archive_path):
    """Distribute an archive to web servers.

    Args:
        archive_path (str): The path to the archive to deploy.

    Returns:
        bool: True if the deployment was successful, False otherwise.
    """
    if not os.path.exists(archive_path):
        print(f'Archive path {archive_path} does not exist.')
        return False

    folder = os.path.basename(archive_path).split('.')[0]

    try:
        # Upload the archive to /tmp/
        put(archive_path, '/tmp/')

        # Create directory for the new release
        run(f'sudo mkdir -p /data/web_static/releases/{folder}')

        # Uncompress the archive to the release folder
        run(f'sudo tar -xzf /tmp/{folder}.tgz -C\
        /data/web_static/releases/{folder}')

        # Remove the archive from /tmp/
        run(f'sudo rm /tmp/{folder}.tgz')

        # Move files and clean up
        run(f'sudo mv /data/web_static/releases/{folder}/web_static/*\
        /data/web_static/releases/{folder}')
        run(f'sudo rm -rf /data/web_static/releases/{folder}/web_static')

        # Update the symbolic link
        run(f'sudo ln -sf /data/web_static/releases/{folder}\
        /data/web_static/current')

    except Exception as e:
        print(f'Error deploying archive: {e}')
        return False

    print('New version deployed!')
    return True


def deploy():
    """Create an archive and deploy it to the web servers.

    Returns:
        bool: True if the deployment was successful, False otherwise.
    """
    archive_path = do_pack()
    if archive_path:
        return do_deploy(archive_path)
    return False
