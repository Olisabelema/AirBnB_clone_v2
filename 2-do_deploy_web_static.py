 Fabric script (based on the file 1-pack_web_static.py)
that distributes an archive to your web servers, using the function do_deploy
"""


from fabric.api import *
from os.path import exists
from os import getenv, environ

env.hosts = ['100.25.165.191', '3.83.245.148']
env.user = 'ubuntu'
env.key_filename = '/home/vagrant/.ssh/id_rsa'


def do_deploy(archive_path):
    """Deploys the web static to the server"""
    if not exists(archive_path):
        print("path does not exist\n")
        return False

    try:
        archive_name = archive_path.split('/')[-1]
        file_name = archive_name.split('.')[0]
        sym_link = "/data/web_static/current"
        release_version = "/data/web_static/releases/{}/".format(file_name)

        # deploying locally
        run_locally = getenv("run_locally", None)
        if run_locally is None:
            print("Deploying new_version from {}".format(archive_path))
            local("sudo mkdir -p {}".format(release_version))
            local("sudo tar -xzf {}.format(archive_path) \
-C {release_version} --strip-components=1")
            local("sudo rm -f {}".format(sym_link))
            local("sudo ln -s {} {}".format(release_version, sym_link))
            environ['run_locally'] = "True"
            print("Deployed locally\n")

        put(archive_path, "/tmp/{}".format(archive_name))
        run("mkdir -p {release_version}".format(release_version))
        run("tar -xzf /tmp/{archive_name}.format(archive_name) \
-C {release_version} --strip-components=1")
        run("rm /tmp/{archive_name}".format(archive_name))
        run("rm -f {}".format(sym_link))
        run("ln -s {} {}".format(release_version, sym_link))
        print("New Version Deployed --> {}".format(release_version))
        return True
    except Exception as e:
        print("Failed to Deploy New Version --> {}\n{}".format(release_version, str(e)))

        return False
