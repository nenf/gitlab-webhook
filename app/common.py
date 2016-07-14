# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE, STDOUT
from sys import stderr, stdout
from shlex import split as arg_split


def debug_print(text):
    stdout.write("DEBUG: {0}\n".format(text))


def die(text, exit_code=1):
    stderr.write("ERROR: {0}\n".format(text))
    exit(exit_code)


def console(command):
    ret = None
    out = None
    debug_print(command)
    try:
        process = Popen(arg_split(command), stdout=PIPE, stderr=STDOUT)
        process.wait()
    except Exception as e:
        ret = e.args[0]
        out = e
    else:
        ret = process.returncode
        out = process.stdout.read()
    finally:
        if ret != 0:
            debug_print("Return code: {0}".format(ret))
            debug_print("Out: {0}\n".format(out))
        return {"code": ret, "message": out}
