#!usr/bin/python3
#-*- coding: utf-8 -*-

import asyncio, sys
import types

from . import background_task
from . import lmdb_utils

def arg_list(flag, argv):
    argv_l = []
    for index in range(argv.index(flag) + 1, len(argv)):
        if argv[index].startswith('-'):
            break
        argv_l.append(argv[index])
    return argv_l


async def script_exec(contnet):
    try:
        proc = await asyncio.create_subprocess_exec(
            sys.executable, '-c', contnet,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await proc.communicate()
        # result = f'[{contnet!r} exited with {proc.returncode}]\n\n'
        result = f'[exited with {proc.returncode}]\n\n'
        if stdout:
            result += f'[stdout]\n{stdout.decode()}'
        if stderr:
            result += f'[stderr]\n{stderr.decode()}'
        # data = await proc.stdout.read()
        # result = data.decode('utf-8').rstrip()
        await proc.wait()
        return {'status': True, 'msg': result}
    except BaseException as e:
        return {'status': False, 'msg': e}


def import_code(code, name):
    # create blank module
    module = types.ModuleType(name)
    # populate the module with code
    exec(code, module.__dict__)
    return module

def resource_name(url):
    url = url.split('?', 1)[0] if '?' in url else url
    url = url.split('&', 1)[0] if '&' in url else url
    return url.rsplit('/', 1)[1] if '/' in url else url
