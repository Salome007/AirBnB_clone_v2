#!/usr/bin/python3
"""
Fabfile to distribute an archive to a web server.
execute: fab -f 2-do_deploy_web_static.py do_deploy:\
    archive_path=folder/file.tgz -i ssh_key -u user
"""
from os import path
# from dotenv import load_dotenv
from fabric.api import env
from fabric.api import put
from fabric.api import run

env.hosts = ["54.161.238.31", "3.85.1.142"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa"


# # load env variable
# if load_dotenv():
#     env.hosts = [getenv('SERVER_1'), getenv('SERVER_2')]
#     env.user = getenv('REMOTE_USER')
#     env.key_filename = getenv('SECRET_KEY')


def do_deploy(archive_path):
    """Distributes an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if path.isfile(archive_path) is False:
        return False
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(file, name)).failed is True:
        return False
    if run("rm /tmp/{}".format(file)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(name, name)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(name)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(name)).failed is True:
        return False
    return True
