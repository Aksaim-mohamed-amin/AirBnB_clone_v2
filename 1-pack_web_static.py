#!/usr/bin/python3
"""
generates a .tgz archive from the contents of the web_static folder of
AirBnB Clone repo
"""

from datetime import datetime
from fabric.api import local


def do_pack():
    """
    archive the web static folder
    """
    rs = local("mkdir -p versions")
    if rs.failed is True:
        return None

    archive_name = f"web_static_{datetime.now().strftime('%Y%m%d%H%M%S')}.tgz"
    rs = local("tar -cvzf versions/%s web_static" % archive_name)
    if rs.failed is True:
        return None

    return f"versions/{archive_name}"
