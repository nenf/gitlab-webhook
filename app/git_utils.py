# -*- coding: utf-8 -*-
from os import path
from common import console


class GitException(Exception):
    def __init__(self, value, code):
        self.value = value
        self.code = code

    def __str__(self):
        return repr(self.value)


class GitUtils:
    def __init__(self):
        pass

    @staticmethod
    def die(text, exit_code=1):
        raise GitException("[ERROR GitUtils] : {0}\n".format(text), exit_code)

    @staticmethod
    def clone(project_name, repository_url):
        if path.exists(project_name):
            return 0
        command = "git clone {0} {1}".format(repository_url, project_name)
        res = console(command, True)
        if res["code"] != 0:
            GitUtils.die(res["message"], res["code"])

    @staticmethod
    def fetch(path_to_repo=None):
        if path_to_repo:
            command = "git -C {0} fetch origin".format(path_to_repo)
        else:
            command = "git fetch origin"
        res = console(command, True)
        if res["code"] != 0:
            GitUtils.die(res["message"], res["code"])

    @staticmethod
    def pull(path_to_repo=None):
        if path_to_repo:
            command = "git -C {0} pull".format(path_to_repo)
        else:
            command = "git pull"
        res = console(command, True)
        if res["code"] != 0:
            GitUtils.die(res["message"], res["code"])

    @staticmethod
    def checkout(commit_id, path_to_repo=None):
        if path_to_repo:
            command = "git -C {0} checkout {1}".format(path_to_repo, commit_id)
        else:
            command = "git checkout {0}".format(commit_id)
        res = console(command, True)
        if res["code"] != 0:
            GitUtils.die(res["message"], res["code"])

    @staticmethod
    def init():
        command = "git init"
        res = console(command, True)
        if res["code"] != 0:
            GitUtils.die(res["message"], res["code"])

    @staticmethod
    def remote_add(remote_repository):
        command = "git remote add origin {0}".format(remote_repository)
        res = console(command, True)
        if res["code"] != 0:
            GitUtils.die(res["message"], res["code"])

    @staticmethod
    def add(files):
        command = "git add {0}".format(files)
        res = console(command, True)
        if res["code"] != 0:
            GitUtils.die(res["message"], res["code"])

    @staticmethod
    def commit(commit_message):
        command = "git commit -m '{0}'".format(commit_message)
        res = console(command, True)
        if res["code"] != 0:
            GitUtils.die(res["message"], res["code"])

    @staticmethod
    def push(push_command):
        command = "git push {0}".format(push_command)
        res = console(command, True)
        if res["code"] != 0:
            GitUtils.die(res["message"], res["code"])

    @staticmethod
    def rev_parse(rev_parse_argument, path_to_repo=None):
        if path_to_repo:
            command = "git -C {0} rev-parse {1}".format(path_to_repo, rev_parse_argument)
        else:
            command = "git rev-parse {0}".format(rev_parse_argument)
        res = console(command)
        if res["code"] != 0:
            GitUtils.die(res["message"], res["code"])
        return res["message"].rstrip()

    @staticmethod
    def log(commit_id, path_to_repo=None):
        if path_to_repo:
            command = "git -C {0} log -n 1 {1}".format(path_to_repo, commit_id)
        else:
            command = "git log -n 1 {0}".format(commit_id)
        res = console(command)
        if res["code"] != 0:
            GitUtils.die(res["message"], res["code"])
        return res["message"].rstrip()

    @staticmethod
    def short_log(commit_id, path_to_repo=None):
        if path_to_repo:
            command = "git -C {0} log --pretty=oneline --format='%h %s' -n 1 {1}".format(path_to_repo, commit_id)
        else:
            command = "git log --pretty=oneline --format='%h %s' -n 1 {0}".format(commit_id)
        res = console(command)
        if res["code"] != 0:
            GitUtils.die(res["message"], res["code"])
        return res["message"].rstrip()

    @staticmethod
    def get_count_commits(branch, path_to_repo=None):
        if path_to_repo:
            command = "git -C {0} rev-list --branches {1} --count".format(path_to_repo, branch)
        else:
            command = "git rev-list --branches {0} --count".format(branch)
        res = console(command)
        if res["code"] != 0:
            GitUtils.die(res["message"], res["code"])
        return res["message"].rstrip()
