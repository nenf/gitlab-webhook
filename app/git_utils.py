# -*- coding: utf-8 -*-
from os import path
from common import console


def git_clone(project_name, repository_url):
    if not path.exists(project_name):
        command = "git clone {0}".format(repository_url)
        return console(command)
    return {"code": 0, "message": "{0} exist".format(project_name)}


def git_fetch(path_to_project):
    command = "git -C {0} fetch origin".format(path_to_project)
    return console(command)


def git_commit_message(path_to_repository, commit_id):
    command = "git -C '{0}' log --format=%B -n 1 {1}".format(path_to_repository, commit_id)
    return console(command)


def git_log(path_to_repository, commit_id):
    command = "git -C '{0}' log -n 1 {1}".format(path_to_repository, commit_id)
    return console(command)


def git_short_log(path_to_repository, commit_id):
    command = "git -C '{0}' log --pretty=oneline --format='%h %s' -n 1 {1}".format(path_to_repository, commit_id)
    return console(command)
