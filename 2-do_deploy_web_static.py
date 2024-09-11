#!/usr/bin/python3
"""distributes an archive to web servers"""

from fabric.api import env, put, run
import os

env.hosts = ['100.25.157.136', '54.237.118.245']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'

def do_deploy(archive_path):
    """distributes an archive to web servers"""
    if not os.path.exists(archive_path):
        return False

    tgz_file = archive_path.split('/')[1]
    folder = tgz_file.split('.')[0]

    try:
        put(archive_path, f"/tmp/")

        run(f"sudo mkdir -p /data/web_static/releases/{folder}/")

        run(f"sudo tar -xzf /tmp/{tgz_file} \
        -C /data/web_static/releases/{folder}/")

        run(f"sudo rm -rf /tmp/{tgz_file}")

        run(f"sudo mv  /data/web_static/releases/{folder}/web_static/* \
        /data/web_static/releases/{folder}/")

        run(f"sudo rm -rf /data/web_static/releases/{folder}/web_static")

        run(f"sudo rm -rf /data/web_static/current")

        run(f"sudo ln -s /data/web_static/releases/{folder}/ \
        /data/web_static/current")

    except Exception as e:
        print('Error:', e)
        return False

    print('New version deployed!')
    return True
