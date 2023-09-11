#!/usr/bin/python3
"""
 a Fabric script that generates a .tgz archive
 from the contents of the web_static folder of your
 AirBnB Clone repo, using the function do_pack
"""
from fabric.api import *
from datetime import datetime


def do_pack():
    """ Generates a .tgz archive from the folder web_static folder
    """
    local("mkdir -p versions")

    date = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = f"versions/web_static_{date}.tgz"

    result = local(f"tar -cvzf {archive_name} web_static")
    if result.succeeded:
        return archive_name
    else:
        return None
