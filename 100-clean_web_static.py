#!/usr/bin/python3
"""Compress and deploy web static package."""
from fabric.api import env, local, put, run
from datetime import datetime
import os

# Define the hosts, user, and key file globally
env.hosts = ['100.25.157.136', '54.237.118.245']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_clean(number=0):
    """deletes out-of-date archives"""
    number = int(number)
    if number <= 0:
        number = 1

    # clean Localhost
    if os.path.exists('versions'):
        local(f'cd versions && ls -t | tail -n +{number + 1}\
        | xargs sudo rm -rf')

    # clean remote server
    try:
        run(f'cd /data/web_static/releases && ls -t |\
        tail -n +{number+1} | xargs sudo rm -rf', pty=False)
    except Exception as e:
        print(f"Error cleaning remote archives on {host}: {e}")
