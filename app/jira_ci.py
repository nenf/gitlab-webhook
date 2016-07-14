# -*- coding: utf-8 -*-
from jira import JIRA
from jira.exceptions import JIRAError
from sys import version_info


class JiraCI:
    resolution_state = {"fixed": "1", "wont fixed": "2", "duplicate": "3", "incomplete": "4", "cannot reproduce": "5",
                        "not a bug": "6", "done": "7"}

    def __init__(self, jira_url, login, password):
        if version_info[1] <= 6:
            options = jira_url
        else:
            options = {"server": jira_url}
        self.jira = JIRA(options, basic_auth=(login, password))

    def check_issue_exist(self, issue_id):
        try:
            self.jira.issue(issue_id)
        except JIRAError as e:
            print "[-] : {0} - {1}".format(issue_id, e.text)
            return False
        else:
            return True

    def check_issue_state(self, issue_id, issue_state):
        jira_issue = self.jira.issue(issue_id)
        if jira_issue.fields.status.name.lower() == issue_state.lower():
            return True
        else:
            return False

    def add_comment(self, issue_id, comment, formatting=False):
        jira_issue = self.jira.issue(issue_id)
        if formatting:
            comment = "{code}" + comment + "{code}"
        if not self.check_comment_exist(issue_id, comment):
            self.jira.add_comment(jira_issue, comment)
            print "[DEBUG JIRA] : Comment (for {0}) : {1} added".format(issue_id, comment.rstrip())
        else:
            print "[DEBUG JIRA] : Comment (for {0}) : {1} already exist".format(issue_id, comment.rstrip())

    def assign_issue(self, issue_id, assigned_user):
        jira_issue = self.jira.issue(issue_id)
        jira_issue.update(assignee={"name": assigned_user})

    def add_link(self, issue_id, title, url):
        url_object = {"url": url, "title": title}
        if not self.check_link_exist(issue_id, title, url):
            self.jira.add_remote_link(issue_id, url_object)
            print "[DEBUG JIRA] : Link (for {0}) : {1} added".format(issue_id, url)
        else:
            print "[DEBUG JIRA] : Link (for {0}) : {1} already exist".format(issue_id, url)

    def resolve_issue_to_reporter(self, issue_id):
        reporter = self.get_reporter_issue(issue_id)
        self.jira.transition_issue(issue_id, "5", resolution={"id": self.resolution_state["fixed"]})
        self.assign_issue(issue_id, reporter)

    def get_reporter_issue(self, issue_id):
        jira_issue = self.jira.issue(issue_id)
        return jira_issue.fields.reporter.name

    def check_comment_exist(self, issue_id, new_comment):
        comments = [c.body for c in self.jira.comments(issue_id)]
        if new_comment in comments:
            return True
        return False

    def check_link_exist(self, issue_id, title, url):
        links = [l.raw["object"] for l in self.jira.remote_links(issue_id)]
        for link in links:
            if link["title"] == title and link["url"] == url:
                return True
        return False

    def resolve_from_git(self, issue_id, short_commit_message, title_url, package_url):
        if self.check_issue_exist(issue_id):
            if not self.check_issue_state(issue_id, "resolved"):
                self.resolve_issue_to_reporter(issue_id)
                print "[DEBUG JIRA] : Issue {0} already resolve".format(issue_id)
            else:
                print "[DEBUG JIRA] : Issue {0} resolved".format(issue_id)
            self.add_link(issue_id, title_url, package_url)
            self.add_comment(issue_id, short_commit_message, formatting=True)

    def refer_from_git(self, issue_id, commit_message):
        if self.check_issue_exist(issue_id):
            self.add_comment(issue_id, commit_message, formatting=True)
