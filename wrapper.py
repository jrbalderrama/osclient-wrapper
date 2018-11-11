import logging
import os
import random
import signal
import sys
import subprocess


logger = logging.getLogger(__name__)


def _configure_logging(args):
    if '-vv' in args:
        logging.basicConfig(level=logging.DEBUG)
        args.remove('-vv')
    elif '-s' in args:
        logging.basicConfig(level=logging.ERROR)
        args.remove('-s')
    elif '--silent' in args:
        logging.basicConfig(level=logging.ERROR)
        args.remove('--silent')
    else:
        logging.basicConfig(level=logging.INFO)
    return args


def _get_scope_et_all(args):
    scope = None
    if '--scope' in args:
        index = args.index('--scope')
        args.remove('--scope')
        scope = args.pop(index)
    return scope, args[1:]


def _run_openstack(port, args):
    url = "http_proxy='http://localhost:{}'".format(port)

    # http_proxy='http://localhost:YOUR_RANDOM_PORT" OPENSTACK_REQUEST
    proxy_prefixed_command = [url] + args
    stdout = subprocess.run(proxy_prefixed_command,
                            shell=True, check=True, stdout=True)
    logger.debug(stdout)

import psutil

def _run_proxy_server(port):
    # mitmdump -s ../proxy_add_headers.py -p RANDOM_PORT
    logging.info("Launching ephemeral proxy server")
    process = subprocess.Popen(['mitmdump',
                                '--script', 'mitmdump_script.py',
                                '--listen-port', str(port)],
                               preexec_fn=os.setsid,
                               stderr=subprocess.STDOUT)
    return process


def _kill_proxy_server(process):

    process_ = psutil.Process(process.pid)
    # for proc in process_.children(recursive=True):
    #     proc.kill()
    # process_.kill()
    os.killpg(os.getpgid(process.pid), signal.SIGHUP)
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)

import time

def main(args):
    nolog_args = _configure_logging(args)
    scope, openstack_args = _get_scope_et_all(nolog_args)
    logger.debug(scope)
    logger.debug(openstack_args)
    port = random.randint(1025, 65535)
    # port = 9192
    process = _run_proxy_server(port)
    print(psutil.Process(process.pid).status())
    time.sleep(2)
    print(psutil.Process(process.pid).status())
    logger.debug(openstack_args)
    _run_openstack(port, openstack_args)
    print(psutil.Process(process.pid).status())
    _kill_proxy_server(process)
    print(psutil.Process(process.pid).status())


if __name__ == "__main__":
    main(sys.argv)
