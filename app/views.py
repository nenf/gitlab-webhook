# -*- coding: utf-8 -*-
from flask.ext.api import status
from json import loads
from flask import request
from app import app
from bug_id_parser import parse_resolve_id, parse_refer_id
from jira_ci import JiraCI
from jira.exceptions import JIRAError
from git_utils import GitUtils, GitException
from re import search
from config import *


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
    git_dir = project_name

    try:
        jira = JiraCI(JIRA_SERVER, JIRA_USER, JIRA_PASSWORD)
    except JIRAError as e:
        return e.text, status.HTTP_400_BAD_REQUEST

    try:
        git = GitUtils()
        git.clone(git_dir, repository_url)
        git.fetch(git_dir)
    except GitException as e:
        return e.value, status.HTTP_400_BAD_REQUEST

    commits_id = [commit["id"] for commit in data["commits"]]
    for commit_id in commits_id:
        try:
            commit_message = git.log(commit_id, git_dir)
            short_log = git.short_log(commit_id, git_dir)
        except GitException as e:
            return e.value, status.HTTP_400_BAD_REQUEST

        resolve_id = parse_resolve_id(commit_message)
        refer_id = parse_refer_id(commit_message)
        package_url = "{0}/{1}/{1}-{2}.zip".format(FILE_SERVER, project_name, commit_id)
        title_url = "{0}-{1}.zip".format(project_name, commit_id)

        for issue_id in resolve_id:
            jira.resolve_from_git(issue_id, short_log, title_url, package_url)

        for issue_id in refer_id:
            jira.refer_from_git(issue_id, commit_message)

    return "Ok", status.HTTP_200_OK
