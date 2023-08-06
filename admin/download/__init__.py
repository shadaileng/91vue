# -*- coding: utf-8 -*-

import sys
import asyncio
import logging

from . import utils
from .utils import add_header, get_resource_size, resource_name
from .apis import Download, thumbnails


def run(task):
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(asyncio.wait([task]))
    except KeyboardInterrupt as e:
        logging.warning('[Stop]')
        print(asyncio.gather(*asyncio.Task.all_tasks()).cancel())
        # 需要先stop循环
        loop.stop()
    except BaseException as e:
        logging.error('[line: %s]' % sys.exc_info()[2].tb_lineno)
        logging.error('[BaseException] %s' % e)
        raise e
    finally:
        # 统一关闭
        loop.run_until_complete(asyncio.sleep(0))
        loop.close()


def download_file_range(url, filename, **kw):
    run(Download(**kw).download_file_range(url, filename))


def download_file_mulity(tasks=[], *, blocks=1, thread_num=1, **kw):
    run(Download(blocks=blocks, thread_num=thread_num, **kw).download_file_mulity(tasks))


def download_m3u8(url, filename, **kw):
    run(Download(**kw).download_m3u8(url, filename))
