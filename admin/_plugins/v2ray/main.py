#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import logging
import json
import re
import hashlib
import time
import asyncio
import base64
from datetime import datetime

from sqlalchemy import func
import aiohttp
from aiohttp_socks import ProxyType, ProxyConnector, ChainProxyConnector

from . import db


def filter_fields_dict(item, fields=[]):
    return {key: val for key, val in item.items() if key in fields}


def filter_fields_dict_list(items, fields=[]):
    return [filter_fields_dict(item, fields) for item in items]


def _download(url, *, filename=None, timeout=300, proxy='', headers={}, chunk_size=1024, dump=True):
    event_loop = asyncio.get_event_loop()
    return_value = None
    try:
        return_value = event_loop.run_until_complete(
            download(url, filename=filename, timeout=timeout, proxy=proxy,
                     headers=headers, chunk_size=chunk_size, dump=dump)
        )
    finally:
        event_loop.close()
    return return_value


async def download(url, *, filename=None, timeout=120, proxy=None, headers={}, chunk_size=1024, dump=True):
    timeout_ = {'total': 60*2, 'connect': None,
                'sock_connect': None, 'sock_read': None}
    if isinstance(timeout, int):
        timeout_ = {'total': timeout, 'connect': None,
                    'sock_connect': None, 'sock_read': None}
    elif isinstance(timeout, dict):
        timeout_ = dict(timeout, **timeout)
    timeout = aiohttp.ClientTimeout(**timeout_)

    connector = aiohttp.TCPConnector(verify_ssl=False)
    logging.info('[+]proxy: %s' % proxy)
    if proxy:
        connector = ProxyConnector.from_url(proxy, verify_ssl=False)
    logging.info('[get]%s' % url)
    result = {'size': 0, 'duration': 0, 'exception': ''}
    start = time.time()
    async with aiohttp.ClientSession(connector=connector, timeout=timeout, trust_env=True) as session:
        try:
            async with session.get(url, headers=headers) as resp:
                result['duration'] = time.time() - start
                curre_size = 0
                total_size = 0
                if resp.status == 206:
                    # Content-Range: bytes 0-499/22400
                    content_range = resp.headers.get('Content-Range', 0)
                    if content_range:
                        exp = re.match(
                            'bytes (\d*)-(\d*)/(\d*)', content_range)
                        if exp:
                            curre_size = int(exp.group(2))
                            total_size = int(exp.group(2)) - int(exp.group(1))
                    else:
                        total_size = int(resp.headers.get('Content-Length', 0))
                if resp.status == 200:
                    total_size = int(resp.headers.get('Content-Length', 0))
                if filename is not None:
                    if not os.path.exists(filename):
                        fp = open(filename, "wb")
                        fp.truncate(total_size + 1)
                        fp.close()
                    with open(filename, "r+b") as fp:
                        fp.seek(curre_size, 0)
                        while True:
                            chunk = await resp.content.read(chunk_size)
                            if not chunk:
                                result['size'] = curre_size
                                break
                            fp.write(chunk)
                            curre_size += len(chunk)
                else:
                    filename = ''
                    while True:
                        chunk = await resp.content.read(chunk_size)
                        if not chunk:
                            result['size'] = len(filename)
                            break
                        filename += chunk.decode('utf8', errors='ignore')
        except aiohttp.client_exceptions.ClientConnectorError as e:
            logging.error(f'[ClientConnectorError]: {e.message}')
            result['exception'] = repr(e)
            result['duration'] = -1
        except aiohttp.client_exceptions.ServerDisconnectedError as e:
            logging.error(f'[ServerDisconnectedError]: {e.message}')
            result['exception'] = repr(e)
            result['duration'] = -1
        except asyncio.TimeoutError as e:
            logging.error(f'[TimeoutError]: {e}')
            result['exception'] = repr(e)
            result['duration'] = -1
        except ConnectionResetError as e:
            logging.error(f'[ConnectionResetError]: {e}')
            result['exception'] = repr(e)
            result['duration'] = -1
        except BaseException as e:
            logging.error(f'[BaseException]: {repr(e)}')
            result['exception'] = repr(e)
            result['duration'] = -1
    logging.info('download %s -> %s(%sb)' %
                 (url, filename[:32] if filename else filename, result))
    return filename, result


def base64_decode(text=b''):
    return base64.decodebytes(text).decode("utf-8", errors='ignore')


def base64_decode_file(filename=''):
    result = ''
    if (os.path.exists(filename)):
        with open(filename, 'rb') as src:
            result = base64_decode(src.read())
            # result = base64.decodebytes(src.read()).decode("utf-8")
    return result


def save_v2ray(server):
    if not isinstance(server, dict):
        return
    keyRelate = [('url', 'url'), ('protocol', 'protocol'),
                 ('subscribe', 'sub'), ('address', 'add'),
                 ('port', 'port'), ('password', 'password'),
                 ('key', 'id'), ('aid', 'aid'),
                 ('security', 'scy'), ('remarks', 'ps'),
                 ('network', 'net'), ('type', 'type'),
                 ('host', '_'), ('tls', 'tls')]
    session = db.create_session()
    v2ray = session.query(db.V2ray).filter(
        db.V2ray.key == server.get('id', '')).first()
    if not v2ray:
        v2ray = db.V2ray(SNI='', allowInsecure=False)
    for (key1, key2) in keyRelate:
        if server.get(key2, '') != '':
            setattr(v2ray, key1, server[key2])
    if v2ray.id is None:
        session.add(v2ray)
    session.commit()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--download", help="download <url>",
                        action="store_true", dest="is_download", default=False)
    parser.add_argument("--text", help="--text <text>")
    parser.add_argument("--filename", help="--filename <filename>")
    parser.add_argument("--url", help="--url <vemss|ss>")
    parser.add_argument("--proxy", help="--proxy <proxy url>")
    args = parser.parse_args()

    if args.is_download:
        if args.url is None:
            parser.print_help()
            exit(-1)
        result = _download(args.url, filename=args.filename, proxy=args.proxy)
        print(f'{result[0]}\n{result[1]}')
