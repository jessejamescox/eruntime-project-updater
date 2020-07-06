#!/usr/bin/python3
#
# rt_updater.py
#
# program will backup and update the runtime project
# auth: Jesse cox WAGO U.S.A.

import os, json, sys, time
from time import localtime, strftime

my_config = {
    'github_user': '',
    'github_repository' : '',
    'github_password' : '',
    'secure' : 'false',
    'current_version' : '',
    'last_updated': ''
}

# get the current config and version
with open('/etc/rt_updater/config.json') as f_config:
    config_data = json.load(f_config)
    my_config['github_user'] = config_data["github_user"]
    my_config['github_repository'] = config_data["github_repository"]
    my_config['github_password'] = config_data["github_password"]
    my_config['secure']  = config_data["secure"]
    my_config['current_version']  = config_data["current_version"]
    print(my_config)

current_version = my_config['current_version']
git_user = my_config['github_user']
git_repo = my_config['github_repository']

# first curl the file to get the latest release
os.system("rm /etc/rt_updater/git_release.json")
os.system("curl --insecure -o /etc/rt_updater/git_release.json https://api.github.com/repos/" + my_config['github_user'] + "/"+ my_config['github_repository'] +"/releases/latest")
with open('/etc/rt_updater/git_release.json') as f_gitinfo:
    git_data = json.load(f_gitinfo)
    target_version = git_data["tag_name"]

# get the current time 
mytime = strftime("%a, %d %b %Y %H:%M:%S %Z", localtime())

# open and write the log file
f_log=open("/etc/rt_updater/rt_updater.log", "a+")
f_log.write("runtime version check started at %s\r\n" % mytime)
f_log.write("local version is %s\r\n" % current_version)
f_log.write("latest version is %s\r\n" % target_version)
f_log.close()
  
# check the release
if current_version != target_version:
    git_url = ("https://github.com/" + git_user + "/" + git_repo + "/releases/download/" + target_version + "/firmware_backup_codesys.tgz")
    print("downloading new project from account: " + git_user + " fromo repo: " + git_repo + " verion: " + target_version)

    # # get the new release from git
    os.system("wget -q -O /tmp/home.tgz " + git_url)

    # # # stop the runtime
    os.system("/etc/init.d/runtime stop")

    # # # backup the exiisting project
    backup_version = ("rt_backup_v" + current_version + ".tgz")
    os.system("tar -czf /etc/rt_updater/%s /home" % backup_version)
    os.system("rm -r /home/*")

    # # # unpackage the update package to /home
    os.system("tar -xzf /tmp/home.tgz -C /home")

    # # # start the runtime
    os.system("/etc/init.d/runtime start")

    os.system("rm /tmp/home.tgz")
    print("Project Update is Complete to version " + target_version)


    f_log=open("/etc/rt_updater/rt_updater.log", "a+")
    f_log.write("successfully updated project version to %s\r\n" % target_version)
    f_log.close()

    my_config['current_version'] = target_version
    my_config['last_updated'] = mytime
    with open('/etc/rt_updater/config.json', 'w') as config_file:
        json.dump(my_config, config_file, sort_keys=True, indent=4)

else:
    print("Project is already up to date")

    f_log=open("/etc/rt_updater/rt_updater.log", "a+")
    f_log.write("update not required, current version is lattest %s\r\n" % target_version)
    f_log.close()