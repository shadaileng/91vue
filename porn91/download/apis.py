# -*- coding: utf-8 -*-

import os
import sys
import time
import re
import subprocess
import logging
import asyncio
import queue
import aiohttp
import ffmpeg

from Crypto.Cipher import AES
from aiohttp import TCPConnector
from aiohttp_socks import ProxyType, ProxyConnector, ChainProxyConnector

from .utils import byteunit, add_header, dumpdata, loaddata, resource_name

COLS = 100


class Download(object):
    def __init__(self, *, is_text=False, proxy=None, timeout_=None, retry_time=5, headers={}, thread_num=32, desc={}, blocks=512, verbose=False):
        self.headers = headers
        self.verbose = verbose
        self.retry_time = retry_time
        self.thread_num = thread_num
        self.desc = desc
        self.blocks = blocks
        self.is_text = is_text
        self.result = {'run': True, 'task': {}}
        self.tasks = queue.Queue(-1)
        self.loop = None
        self.proxy = proxy
        self.timeout = {'total': 60*5, 'connect': None, 'sock_connect': None, 'sock_read': None}
        if isinstance(timeout_, int):
            self.timeout = {'total': timeout_, 'connect': None, 'sock_connect': None, 'sock_read': None}
        elif isinstance(timeout_, dict):
            self.timeout = dict(self.timeout, **timeout_)

    def set_timeout(self):
        return aiohttp.ClientTimeout(**self.timeout)

    async def download_status(self, filename, speed={'beg_t': 0, 'beg_d': 0, 'dtl': 0}):
        status_file = f'{filename}.json'
        status_msg = f'{filename}.msg.json'
        logging.info(f'[-]output file: {status_file}')
        dumpdata(status_file, self.result)
        msg_result = dumpdata(status_msg, {'_status': True})
        while True:
            # 结束任务
            msg_result = loaddata(status_msg)
            if msg_result and not msg_result.get('_status', True):
                loop = asyncio.get_event_loop()
                logging.warning(f'[Stoping]: {asyncio.gather(*asyncio.Task.all_tasks()).cancel()}')
                # 需要先stop循环
                loop.stop()
                return
            dumpdata(status_file, self.result)
            flag = True
            status_str = ''
            sum = 0.0
            total = 0
            thread_num = 0
            if len(self.result.get('task', {})) > 0:
                for key, item in self.result['task'].items():
                    if key == '_status':
                        continue
                    sum += float(item.get('scale') * 100)
                    total += item.get('size')
                    if item['complete'] == 0 or item['complete'] == -1:
                        flag = False
                    if item['run']:
                        thread_num += 1
                self.desc['size'] = total
                cur = time.time()
                if speed['beg_t'] == 0:
                    speed['beg_d'] = total
                    speed['beg_t'] = cur
                if cur - speed['beg_t'] >= 1:
                    speed['dtl'] = (total - speed['beg_d']) / \
                        (cur - speed['beg_t'])
                    speed['beg_d'] = total
                    speed['beg_t'] = cur
                status_str = '%s(%.2f%%, %s/s) | %d' % (byteunit(total), sum / len(self.result.get('task', {'None': None})), byteunit(speed['dtl']), thread_num)
                status = {'filename': filename, 'total': total, 'scale': sum / len(self.result.get('task', {'None': None})), 'speed': speed['dtl'], 'threadNum': thread_num}
            else:
                status_str = f'[Error] task of result is empty: {self.result}'
                status = {'filename': filename, 'total': total, 'scale': 0, 'speed': speed['dtl'], 'threadNum': thread_num}
            if self.verbose:
                print('status: %s%s' % (status_str, ' ' * (0 if len(status_str) > COLS - 10 else COLS - len(status_str) - 10)), end='\r')
            dumpdata(f'{filename}.status', status)
            dumpdata(os.path.join(os.path.dirname(filename), 'running.status'), status)
            # logging.info(sum / len(self.result.get('task', {'None': None})))
            # logging.info(self.result.get('task', {'None': None}))
            # print('running.status', status)
            if flag:
                break
            await asyncio.sleep(0.1)
        speed = {'beg_t': 0, 'beg_d': 0, 'dtl': 0}
        logging.info(f'[{filename}]download complete')
        try:
            pass
        except BaseException as e:
            logging.error(f'[Error: {sys.exc_info()[2].tb_lineno}]: {e}')

    async def download_task(self, *, headers={}, chunk_size=1024):
        while not self.tasks.empty():
            key = self.tasks.get()
            retry = self.retry_time
            while retry > 0:
                try:
                    task = self.result['task'][key]
                    if task['complete'] > 0:
                        break
                    url = task['url']
                    filename = task['name']
                    if 'range' in task:
                        headers['Range'] = 'bytes=%d-%d' % (task['range'][0] + task['size'], task['range'][1])
                    if asyncio.get_event_loop().is_closed():
                        return
                    # timeout = aiohttp.ClientTimeout(total=self.set_timeout())
                    connector = TCPConnector(verify_ssl=False)
                    if self.proxy:
                        logging.info(f'[+]proxy: {self.proxy}')
                        connector = ProxyConnector.from_url(self.proxy, verify_ssl=False)
                    logging.info(f'[get]{url}')
                    async with aiohttp.ClientSession(connector=connector, timeout=self.set_timeout(), trust_env=True) as session:
                        async with session.get(url, headers=headers) as resp:
                            task['status'] = resp.status
                            task['headers'] = {key: resp.headers[key] for key in resp.headers}
                            if resp.status in (206, 200):
                                current_size = 0
                                if resp.status == 206:
                                    current_size = task['size']
                                total_size = int(resp.headers.get('Content-Length', 0))
                                if 'range' in task:
                                    total_size = task['range'][1] - task['range'][0]
                                if not os.path.exists(filename):
                                    os.makedirs(os.path.dirname(filename), exist_ok=True)
                                    fp = open(filename, "wb")
                                    fp.truncate(total_size + 1)
                                    fp.close()
                                with open(filename, "r+b") as fp:
                                    fp.seek(current_size, 0)
                                    while True:
                                        chunk = await resp.content.read(chunk_size)
                                        if not chunk:
                                            break
                                        fp.write(chunk)
                                        current_size += len(chunk)
                                        task['scale'] = current_size / (total_size if total_size > 0 else current_size)
                                        task['size'] = current_size
                                        # logging.info(f'current_size: {current_size}, total_size: {total_size}, task: {task}, header: {resp.headers}')
                                task['complete'] = 1
                                task['scale'] = 1.00
                            else:
                                err = f"[Error] status: {resp.status}, reason: {resp.reason}"
                                logging.warning(err)
                                task['err'] = err
                                task['complete'] = -2
                    break
                except aiohttp.ServerDisconnectedError as e:
                    text = f"[ServerDisconnectedError]get {task['name']}: {e.message}"
                    logging.error(f'[line: {sys.exc_info()[2].tb_lineno}]')
                    logging.error(text)
                    self.result['task'][key]['complete'] = 2
                    break
                except asyncio.TimeoutError as e:
                    logging.error(f'[line: {sys.exc_info()[2].tb_lineno}]')
                    logging.error(f'[Timeout] {self.result["task"][key]["name"]} remain: {retry - 1}')
                except aiohttp.ClientResponseError as e:
                    logging.error(f'[line: {sys.exc_info()[2].tb_lineno}]')
                    logging.error(f'[ResponseError: {task["name"]}, remain: {retry - 1}] status: {e.status}, message: {e.message}')
                except aiohttp.ClientError as e:
                    logging.error(f'[line: {sys.exc_info()[2].tb_lineno}]: {e}, remain: {retry - 1}')
                # except RuntimeError as e:
                #     logging.error('[line: %s]' % sys.exc_info()[2].tb_lineno)
                #     logging.error('[RuntimeError] %s' % e)
                #     break
                # except BaseException as e:
                #     logging.error('[line: %s]' % sys.exc_info()[2].tb_lineno)
                #     logging.error('[retry] failed to get %s: %s, remain: %s' % (self.result['task'][key]['name'], e, retry - 1))
                retry -= 1
            if retry <= 0:
                self.result['task'][key]['complete'] = 2
            self.result['task'][key]['run'] = False

    def task_load(self, filename):
        data = loaddata(f'{filename}.json')
        if data and len(data.get('task', {})) > 0:
            for key, item in data['task'].items():
                if item['complete'] not in (-1, 0, 1) or item['complete'] == 1 and not os.path.exists(item['name']):
                    item['complete'] = -1
                    item['scale'] = 0
                    item['size'] = 0
                    item['run'] = True
                self.result['task'][key] = item
                self.tasks.put(key)

    async def get_resource_size(self, url, *, headers={}):
        mt = False
        total = 0
        status = False
        msg = ''
        headers['Range'] = 'bytes=0-4'
        connector = TCPConnector(verify_ssl=False)
        if self.proxy:
            logging.info(f'[+]proxy: {self.proxy}')
            connector = ProxyConnector.from_url(self.proxy, verify_ssl=False)
        logging.info(f'[head]{url}')
        try:
            async with aiohttp.ClientSession(connector=connector, timeout=self.set_timeout()) as session:
                async with session.head(url, headers=headers) as resp:
                    resp_headers = resp.headers
                    if resp.status == 206:
                        rex = re.match(r'^bytes 0-4/(\d+)$', resp_headers['Content-Range'])
                        if rex:
                            total = int(rex.group(1))
                            mt = True
                            status = True
                    elif resp.status == 200:
                        total = int(resp_headers.get('Content-Length', '1'))
                        status = True
                    elif resp.status == 301:
                        url = resp_headers.get('Location', None)
                        if url:
                            return await self.get_resource_size(url, headers=headers)
                        else:
                            msg = f'status: {resp.status}, reason: {resp.reason}, Location:{resp_headers.get("Location", None)}'
                    else:
                        msg = f'status: {resp.status}, reason: {resp.reason}'
        except aiohttp.ServerDisconnectedError as e:
            logging.error(f'[line: {e}]')
            msg = f"[ServerDisconnectedError]head {url}: {e.message}"
            logging.error(msg)
        except aiohttp.ServerTimeoutError as e:
            logging.error(f'[line: {e}]')
            msg = f'[Timeout]head {url}: {e.message}'
            logging.error(msg)
        logging.info(f'3[head]{url}')

        return (status, total, mt, msg, url)

    def task_check(self, filename):
        # 成功的结果
        complete = []
        for key, item in self.result['task'].items():
            if item['complete'] == 1:
                if os.path.exists(key):
                    complete.append(item)
                else:
                    self.result['task'][key]['complete'] = -1
                    self.result['task'][key]['size'] = 0
                    self.result['task'][key]['scale'] = 0
                    self.result['task'][key]['run'] = True
        dumpdata(f'{filename}.json', self.result)
        if len(complete) != len(self.result['task']):
            logging.warning(f'Failed to download [{filename}]: {len(complete)}/{len(self.result["task"])}')
            return (False, complete)
        return (True, complete)

    def task_merge(self, filename, complete=[], *, rmts=False):
        # 成功的结果
        if len(complete) <= 0:
            raise BaseException(f'number of complete file is 0: {complete}')
        root, name_ = os.path.split(filename)
        keys = {}
        for item in complete:
            key_dir = os.path.dirname(item['name'])
            if keys.get(key_dir, None):
                keys[key_dir].append((item['name'], item.get('key', None)))
            else:
                keys[key_dir] = [(item['name'], item.get('key', None))]
        for key, items in keys.items():
            name = os.path.join(key, name_)
            if os.path.exists(name):
                os.remove(name)
            logging.info(f'[-]output file: {name}')
            with open(name, 'ab') as dst:
                for index, item in enumerate(items, start=1):
                    if not os.path.exists(item[0]):
                        continue
                    with open(item[0], 'rb') as src:
                        if item[1]:
                            # 解密
                            cryptor = AES.new(
                                item[1].encode(), AES.MODE_CBC, item[1].encode())
                            dst.write(cryptor.decrypt(src.read()))
                        else:
                            dst.write(src.read())
                        if rmts:
                            os.remove(item[0])
                    status_str = f'{str(item)} | ({index} / {len(items)})'
                    if self.verbose:
                        print('merge_status: %s%s' % (status_str, ' ' * (100 - len(status_str))), end='\r')
                    dumpdata(f'{name}.status_merge', status_str)
            if self.verbose:
                print(f'\n[-]output file: {name}')

    async def task_merge_m3u8(self, filename, complete=[], *, rmts=False):
        # 成功的结果
        if len(complete) <= 0:
            raise BaseException(f'number of complete file is 0: {complete}')
        root, name_ = filename.rsplit('/', 1)
        keys = {}
        for item in complete:
            key_dir = os.path.dirname(item['name'])
            if keys.get(key_dir, None):
                keys[key_dir].append((item['name'], item.get('key', None)))
            else:
                keys[key_dir] = [(item['name'], item.get('key', None))]
        for key, items in keys.items():
            name = f'{key}/{name_}'
            if os.path.exists(name):
                os.remove(name)
            # _name = name.rsplit('.', 1)[0]
            _name = filename.rsplit('.', 1)[0]
            if not os.path.exists(f'{_name}.m3u8'):
                logging.error(f'm3u8 file: {_name}.m3u8 not exists')
                continue
            logging.info(f'[-]output file: {name}')
            # command = 'ffmpeg -y -allowed_extensions ALL -protocol_whitelist "file,http,crypto,tcp" -i %s.m3u8 -c copy %s' % (_name, name)
            # -allowed_extensions ALL 根据本地key解密
            command = f'ffmpeg -y -allowed_extensions ALL -i {_name}.m3u8 -c:v copy -c:a copy -bsf:a aac_adtstoasc {filename}'
            logging.info(f'merge mp4\nexec: {command}')
            # result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result = await asyncio.create_subprocess_shell(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = await result.communicate()
            if result.returncode != 0:
                logging.error(stderr)
            if self.verbose:
                print(f'\n[-]output file: {name}')
            duration = await thumbnails(filename, f'{_name}.png')
            if not self.desc.get('duration', False):
                self.desc['duration'] = duration

    async def download_file_range(self, url, filename):
        headers = dict(add_header(text=self.is_text), **self.headers)
        status, total, mt, msg, url = await self.get_resource_size(url, headers=headers)
        if not status:
            logging.error(msg)
            return
        self.desc['size'] = total
        self.task_load(filename)
        if self.tasks.empty():
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            if not mt:
                name = f'{filename}-0'
                self.tasks.put(name)
                task_index = {'name': name, 'url': url, 'scale': 0, 'size': 0, 'run': True, 'complete': 0, 'error': None}
                self.result['task'][name] = task_index
            else:
                logging.info(f'[+]total: {byteunit(total)}, {self.blocks} ts, thread num: {self.thread_num}')
                part = total // self.blocks
                for index in range(self.blocks):
                    name = f'{filename}-{index}'
                    task_index = {'name': name, 'url': url, 'range': (part * index + 1 if index > 0 else part * index, total if index ==
                                                                      self.blocks - 1 else part * index + part), 'scale': 0, 'size': 0, 'run': True, 'complete': 0, 'error': None}
                    self.tasks.put(name)
                    self.result['task'][name] = task_index
        retry = 3
        while retry > 0:
            tasks = [self.download_task(headers=headers) for index in range(self.thread_num)]
            tasks.append(self.download_status(filename))
            await asyncio.gather(*tasks)
            status, complete = self.task_check(filename)
            if status:
                self.task_merge(filename, complete, rmts=True)
                break
            self.task_load(filename)
            retry -= 1
            logging.warning(f'retry: {3 - retry}')
        self.desc['status'] = status

    async def download_file_mulity(self, tasks=[]):
        tasks = [self.download_file_range(url, filename)
                 for url, filename in tasks]
        await asyncio.gather(*tasks)

    async def download_file_mini(self, url, filename, *, headers={}, chunk_size=1024):
        headers = dict(dict(add_header(), **self.headers), **headers)
        # timeout = aiohttp.ClientTimeout(total=self.set_timeout())
        connector = TCPConnector(verify_ssl=False)
        if self.proxy:
            logging.info(f'[+]proxy: {self.proxy}')
            connector = ProxyConnector.from_url(self.proxy, verify_ssl=False)
        logging.info(f'[get]{url}')
        async with aiohttp.ClientSession(connector=connector, timeout=self.set_timeout()) as session:
            async with session.get(url, headers=headers) as resp:
                if resp.status in (206, 200):
                    total_size = int(resp.headers.get('Content-Length', 0))
                    if not os.path.exists(filename):
                        fp = open(filename, "wb")
                        fp.truncate(total_size + 1)
                        fp.close()
                    with open(filename, "r+b") as fp:
                        while True:
                            chunk = await resp.content.read(chunk_size)
                            if not chunk:
                                break
                            fp.write(chunk)
                else:
                    logging.error(f'status: {resp.status}')

    async def download_m3u8(self, url, filename):
        headers = add_header(text=self.is_text)
        filename_tss = f'{filename}_ts'
        self.task_load(filename)
        merge_result = {}
        if self.tasks.empty():
            await self.download_m3u8_load(url, filename, merge_result)
        else:
            for key, item in self.result['task'].items():
                if item['from'] not in merge_result:
                    merge_result[item['from']] = {}
                merge_result[item['from']][key] = item
        # print(merge_result)
        # status_file = '%s.json' % filename
        # dumpdata(status_file, self.result)
        # print(merge_result)
        # return
        tasks = [self.download_task(headers=headers) for index in range(self.thread_num)]
        tasks.append(self.download_status(filename))
        await asyncio.gather(*tasks)

        await self.merge_m3u8(filename, merge_result)
        # status, complete = self.task_check(filename_tss)
        # if not status:
        #     logging.warning('download not complete')
        # if filename.endswith('.m3u8'):
        #     filename = filename.rsplit('.', 1)[0]
        # self.task_merge(filename, complete)

    async def merge_m3u8(self, filename, merge_result={}):
        complete = []
        for key, item in merge_result.items():
            if not key.endswith('.m3u8'):
                if os.path.exists(key):
                    complete.append(item)
            else:
                await self.merge_m3u8(key, item)
        if len(complete) > 0:
            if filename.endswith('.m3u8'):
                filename = f"{os.path.splitext(filename)[0]}.mp4"
            await self.task_merge_m3u8(filename, complete)

    async def download_m3u8_load(self, url, filename, merge_result={}):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        await self.download_file_mini(url, filename)
        if not os.path.exists(filename):
            raise BaseException(f"m3u8 file not exists: {filename}")
        content = ''
        file_line = None
        with open(filename, 'r') as src:
            content = src.read()
        if len(content) <= 0:
            raise BaseException(f"Failed to download m3u8 file: \n{content}")
        if '\r\n' in content:
            file_line = content.split("\r\n")
        else:
            file_line = content.split("\n")
        if file_line[0] != "#EXTM3U":
            raise BaseException(f"it is not m3u8 file: \n{content}")
        tss = []
        duration = 0.0
        key = None
        with open(filename, 'w') as src:
            url_root = '%s%s' % (url[:url.index('://')+3], url[url.index('://')+3:].split('/', 1)[0])
            uri = '/%s' % url[url.index('://')+3:].split('/', 1)[1]
            for line in file_line:
                line = line.strip().strip('\x00')
                if len(line) <= 0:
                    continue
                line__ = None
                if '#EXT-X-KEY' in line:
                    key_uri = re.search('URI="(.*)"', line.replace("'", '"')).group(1) if '"' in line or "'" in line else re.search('URI=(.*)', line).group(1)
                    if key_uri.startswith('/'):
                        key_url = '%s%s' % (url_root, key_uri)
                    elif key_uri.startswith('http'):
                        key_url = key_uri
                    else:
                        key_url = '%s/%s' % (url.rsplit('/', 1)[0], key_uri)
                    key_path = '%s/%s' % (filename.rsplit('/', 1)[0], resource_name(key_uri))
                    await self.download_file_mini(key_url, key_path)
                    with open(key_path, 'r', errors='ignore') as key_src:
                        key = key_src.read()
                    # line = '%sURI="%s"' % (line[:line.index('URI=')], key_uri if '/' not in key_uri else key_uri.rsplit('/', 1)[1])
                    line = line.replace(key_uri, key_uri if '/' not in key_uri else key_uri.rsplit('/', 1)[1])
                if '#EXTINF:' in line:
                    exp = re.match('#EXTINF:(.\d*\.?\d*),', line)
                    duration = duration + float(exp.group(1))
                if line.startswith('/'):
                    index = 0
                    line_ = line.split('/')
                    uri_ = uri.split('/')
                    while (index < min(len(line_), len(uri_))) and line_[index] == uri_[index]:
                        index += 1
                    line = '/'.join(line_[index:])
                    line__ = '%s%s' % (url_root, line)
                # if line.startswith('http'):
                #     line__ = line
                #     line = '/%s' % line[line.index('://') + 3:].split('/', 1)[1]
                #     line_ = line.split('/')
                #     uri_ = uri.split('/')
                #     index = 0
                #     while (index < min(len(line_), len(uri_))) and line_[index] == uri_[index]:
                #         index += 1
                #     line = '/'.join(line_[index:])
                if line.startswith('http'):
                    line__ = line
                    line = '/%s' % line[line.index('://') + 3:].split('/', 1)[1]
                    line_ = line.split('/')
                    uri_ = uri.split('/')
                    index = 0
                    while (index < min(len(line_), len(uri_))) and line_[index] == uri_[index]:
                        index += 1
                    line = '/'.join(line_[index:])
                
                src.write('%s\n' % (line.split('?', 1)[0] if '?' in line else line))
                if "#EXT" in line or len(line.strip()) == 0:
                    continue
                ts_name = line.split('?', 1)[0] if '?' in line else line
                # ts_name = line
                # print(f'line__: {line__}, line: {line}')
                if line__:
                    tss.append((line__, os.path.join(os.path.dirname(filename), ts_name)))
                else:
                    tss.append(('%s/%s' % ((url.split('?', 1)[0] if '?' in url else url).rsplit('/', 1)[0], line), os.path.join(os.path.dirname(filename), ts_name)))
        self.desc['duration'] = duration
        for url, name in tss:
            if name.endswith('.m3u8'):
                merge_result[name] = {}
                await self.download_m3u8_load(url, name, merge_result[name])
            else:
                item = {'name': name, 'url': url, 'scale': 0, 'size': 0, 'run': True, 'complete': 0, 'error': None, 'key': key, 'from': filename}
                self.result['task'][name] = item
                self.tasks.put(name)
                merge_result[name] = item


async def thumbnails(src, dst, frames=80):
    logging.info(f'[+]output file: {dst}')
    def div(s):
        a, b = s.split('/', 1)
        return float(a) / float(b)
    result = [{'duration': float(s['duration']), 'frames': (float(s['duration']) * (div(s['avg_frame_rate'])) / 100) if div(s['avg_frame_rate']) != 0 else int(s['duration']) * 30 / 100} for s in ffmpeg.probe(src)['streams'] if s['codec_type'] == 'video']
    logging.info(f'video info: {result}')
    duration = 0
    if len(result) > 0:
        frames = result[0].get('frames', 0)
        duration = result[0].get('duration', 0)
    frames = int(frames)
    # ffmpeg -y -i 634171.mp4 -vf select='not(mod(n\,60))',scale=160:-1,tile=100x1 -frames:v 1 634171.png
    command = f"ffmpeg -y -i {src} -vf select='not(mod(n\,{frames}))',scale=160:-1,tile=100x1 -frames:v 1 {dst}"
    logging.info(f'gen thumbnails\nexec: {command}')
    # result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = await asyncio.create_subprocess_shell(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = await result.communicate()
    if result.returncode != 0:
        logging.error(stderr)
    logging.info(f'[-]output file: {dst}')
    return duration
