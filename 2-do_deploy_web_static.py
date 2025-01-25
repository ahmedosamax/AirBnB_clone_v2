#!/usr/bin/python3
"""web server distribution"""
from fabric.api import env, put, run
import os

env.hosts = ['100.24.74.65', '54.196.37.18']

def do_deploy(archive_path):
	"""Distributes an archive to the web servers."""
	if not os.path.exists(archive_path):
		return False

	try:
		archive_filename = os.path.basename(archive_path)
		folder_name = archive_filename.split('.')[0]
		release_path = f"/data/web_static/releases/{folder_name}"
		tmp_path = f"/tmp/{archive_filename}"
		put(archive_path, tmp_path)
		run(f"mkdir -p {release_path}")
		run(f"tar -xzf {tmp_path} -C {release_path}")
		run(f"rm {tmp_path}")
		run(f"mv {release_path}/web_static/* {release_path}/")
		run(f"rm -rf {release_path}/web_static")
		run("rm -rf /data/web_static/current")
		run(f"ln -s {release_path} /data/web_static/current")
		return True
	except Exception:
		return False
