# -*- coding: utf-8 -*-
from flask.ext.api import status
from json import loads
from flask import request
from app import app
from bug_id_parser import parse_resolve_id, parse_refer_id
from jira_ci import JiraCI
from jira.exceptions import JIRAError
from git_utils import git_clone, git_fetch, git_log, git_short_log
from config import file_server_url, jira_url, jira_user, jira_password
from re import search


@app.route('/', methods=['POST'])
def index():
    data = loads(request.data)
    if not data:
        return "Ok", status.HTTP_200_OK

    default_branch = data["project"]["default_branch"]
    if not search(".*/{0}".format(default_branch), data["ref"]):
        return "Ok", status.HTTP_200_OK

    project_name = data["project"]["name"]
    repository_url = data["project"]["git_ssh_url"]
    git_dir = data["project"]["name"]
    try:
        jira = JiraCI(jira_url, jira_user, jira_password)
    except JIRAError as e:
        return e.text, status.HTTP_400_BAD_REQUEST

    res = git_clone(git_dir, repository_url)
    if res["code"] != 0:
        return res["message"], status.HTTP_400_BAD_REQUEST

    res = git_fetch(git_dir)
    if res["code"] != 0:
        return res["message"], status.HTTP_400_BAD_REQUEST

    commits = [commit["id"] for commit in data["commits"]]
    for commit_id in commits:
        res = git_log(git_dir, commit_id)
        if res["code"] != 0:
            return res["message"], status.HTTP_400_BAD_REQUEST
        commit_message = res["message"]

        res = git_short_log(git_dir, commit_id)
        if res["code"] != 0:
            return res["message"], status.HTTP_400_BAD_REQUEST
        short_log = res["message"]

        resolve_id = parse_resolve_id(commit_message)
        refer_id = parse_refer_id(commit_message)
        package_url = "{0}/{1}/{1}-{2}.zip".format(file_server_url, project_name, commit_id)
        title_url = "{0}-{1}.zip".format(project_name, commit_id)

        for issue_id in resolve_id:
            jira.resolve_from_git(issue_id, short_log, title_url, package_url)

        for issue_id in refer_id:
            jira.refer_from_git(issue_id, commit_message)

    return "Ok", status.HTTP_200_OK
