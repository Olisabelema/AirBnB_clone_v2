from fabric.api import *
from os.path import exists
from os import getenv, environ

env.hosts = ['100.25.165.191', '3.83.245.148']
env.user = 'ubuntu'
env.key_filename = '/home/vagrant/.ssh/id_rsa'


def do_deploy(archive_path):
    """Deploys the web static to the server"""
    if not exists(archive_path):
        print("Path does not exist\n")
        return False

    try:
        archive_name = archive_path.split('/')[-1]
        file_name = archive_name.split('.')[0]
        sym_link = "/data/web_static/current"
        release_version = "/data/web_static/releases/{}/".format(file_name)

        # Deploying locally
        run_locally = getenv("run_locally", None)
        if run_locally is None:
            print("Deploying new_version from {}".format(archive_path))
            local("sudo mkdir -p {}".format(release_version))
            local("sudo tar -xzf {} -C {} --strip-components=1".format(archive_path, release_version))
            local("sudo rm -f {}".format(sym_link))
            local("sudo ln -s {} {}".format(release_version, sym_link))
            environ['run_locally'] = "True"
            print("Deployed locally\n")

        put(archive_path, "/tmp/{}".format(archive_name))
        run("mkdir -p {}".format(release_version))
        run("tar -xzf /tmp/{} -C {} --strip-components=1".format(archive_name, release_version))
        run("rm /tmp/{}".format(archive_name))
        run("rm -f {}".format(sym_link))
        run("ln -s {} {}".format(release_version, sym_link))
        print("New Version Deployed --> {}".format(release_version))
        return True
    except Exception as e:
        print("Failed to Deploy New Version --> {}\n{}".format(release_version, str(e)))
        return False
