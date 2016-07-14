# -*- coding: utf-8 -*-
from re import findall

suffix = "Resolve:"
pattern_bug_id = r"{0}\s+([a-zA-Z]*-[0-9]*)".format(suffix)

suffix = "Refer:"
pattern_ref_bug_id = r"{0}\s+([a-zA-Z]*-[0-9]*)".format(suffix)


def parse_resolve_id(commit_message):
    return findall(pattern_bug_id, commit_message)


def parse_refer_id(commit_message):
    return findall(pattern_ref_bug_id, commit_message)


def print_bug_id(l_bugs, s_commit):
    if not l_bugs:
        return 0
    s_bugs = "".join("{0} ".format(bug) for bug in l_bugs)
    print "{0}: {1}".format(s_commit, s_bugs)
