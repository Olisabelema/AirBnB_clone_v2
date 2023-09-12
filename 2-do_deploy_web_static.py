#!/usr/bin/python3
"""
 a Fabric script that generates a .tgz archive
 from the contents of the web_static folder of your
 AirBnB Clone repo, using the function do_pack
"""
from fabric.api import *
from datetime import datetime
from os.path import exists
from os import getenv, environ

def do_pack():
    """ Generates a .tgz archive from the folder web_static folder
    """
    local("mkdir -p versions")

    date = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = "versions/web_static_{}.tgz".format(date)

    result = local("tar -cvzf {} web_static".format(archive_name))
    if result.succeeded:
        return archive_name
    else:
        return None

"""
a Fabric script (based on the file 1-pack_web_static.py)
that distributes an archive to your web servers, using the function do_deploy
"""

env.hosts = ['100.25.165.191', '3.83.245.148']
env.user = 'ubuntu'
env.key_filename = '/home/root/.ssh/id_rsa'


def do_deploy(archive_path):
    """Deploys the web static to the server"""
    if not exists(archive_path):
        print("path does not exist\n")
        return False

    try:
        archive_name = archive_path.split('/')[-1]
        file_name = archive_name.split('.')[0]
        sym_link = "/data/web_static/current"
        release_version = f"/data/web_static/releases/{file_name}/"

        # deploying locally
        run_locally = getenv("run_locally", None)
        if run_locally is None:
            print(f"Deploying new_version from {archive_path}")
            local(f"sudo mkdir -p {release_version}")
            local(f"sudo tar -xzf {archive_path} \
-C {release_version} --strip-components=1")
            local(f"sudo rm -f {sym_link}")
            local(f"sudo ln -s {release_version} {sym_link}")
            environ['run_locally'] = "True"
            print("Deployed locally\n")

        put(archive_path, f"/tmp/{archive_name}")
        run(f"mkdir -p {release_version}")
        run(f"tar -xzf /tmp/{archive_name} \
-C {release_version} --strip-components=1")
        run(f"rm /tmp/{archive_name}")
        run(f"rm -f {sym_link}")
        run(f"ln -s {release_version} {sym_link}")
        print(f"New Version Deployed --> {release_version}")
        return True
    except Exception as e:
        print(f"Failed to Deploy New Version --> {release_version}\n{str(e)}")
        return False
