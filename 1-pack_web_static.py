from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """
    generates a .tgz archive from the contents of the web_static folder
    of AirBnB Clone repo
    """
    # Create the versions directory
    if not os.path.exists('versions'):
        os.mkdir('versions')

    # Get the current time stamp and create the archive name
    now = datetime.now()
    archive_name = f"versions/web_static_{now.strftime('%y%m%d%H%M%S')}.tgz"

    # Create the .tgz archive for the web_static folder
    print(f"Packing web_static to {archive_name}")
    result = local(f"tar -cvzf {archive_name} web_static")

    if result.failed:
        return None
    return archive_name
