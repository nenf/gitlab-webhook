# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE, STDOUT
from sys import stdout
from shlex import split as arg_split


def debug(text):
    stdout.write("[DEBUG]: {0}\n".format(text))


def console(command, stream=False):
    ret = None
    out = None
    debug(command)
    try:
        process = Popen(arg_split(command), stdout=PIPE, stderr=STDOUT)
        if stream:
            for line in iter(process.stdout.readline, b""):
                print line.rstrip()
        process.wait()
    except Exception as e:
        ret = e.args[0]
        out = e
    else:
        ret = process.returncode
        out = process.stdout.read()
    finally:
        return {"code": ret, "message": out}

