# -*- coding: utf-8 -*-

import os, sys, time, re
import logging
import asyncio
import queue
import aiohttp

from aiohttp_socks import ProxyType, ProxyConnector, ChainProxyConnector

from .utils import byteunit, get_resource_size, add_header, dumpdata, loaddata, save_file, resource_name, resource_fullname

COLS = 100


class Download(object):
    def __init__(self, task=[], *, is_text=False, timeout_=60, retry_time=50, headers={}, thread_num=32, verbose=False):
        self.timeout_ = timeout_
        self.headers = headers
        self.timeout_ = timeout_
        self.verbose = verbose
        self.retry_time = retry_time
        self.thread_num = thread_num
        self.is_text = is_text
        self.result = {'run': True, 'task': {}}
        self.tasks = queue.Queue(-1)
        self.loop = None

    async def download_status(self, filename, speed={'beg_t': 0, 'beg_d': 0, 'dtl': 0}):
        try:
            status_file = '%s.json' % filename
            logging.info('[-]output file: %s' % status_file)
            dumpdata(status_file, self.result)
            while True:
                # 结束任务
                # tmp_result = loaddata(status_file)
                # if tmp_result and not tmp_result.get('_status', True) and loop:
                #     logging.warning('[Stoping]')
                #     loop.stop()
                #     loop.run_forever()
                #     logging.warning('[Stoped]')
                #     break
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
                    cur = time.time()
                    if speed['beg_t'] == 0:
                        speed['beg_d'] = total
                        speed['beg_t'] = cur
                    if cur - speed['beg_t'] >= 1:
                        speed['dtl'] = (total - speed['beg_d']) / (cur - speed['beg_t'])
                        speed['beg_d'] = total
                        speed['beg_t'] = cur
                    status_str = '%s(%.2f%%, %s/s) | %d' % (byteunit(total), sum / len(
                        self.result.get('task', {'None': None})), byteunit(speed['dtl']), thread_num)
                else:
                    status_str = '[Error] task of result is empty: %s' % self.result
                if self.verbose:
                    print('status: %s%s' % (status_str, ' ' * (0 if len(status_str) > COLS - 10 else COLS - len(status_str) - 10)), end='\r')
                dumpdata('%s.status' % filename, status_str)
                if flag:
                    break
                await asyncio.sleep(0.1)
            print("")
            speed = {'beg_t': 0, 'beg_d': 0, 'dtl': 0}
            logging.info('\ndownload complete')
        except BaseException as e:
            logging.error('[Error: %s]: %s' % (sys.exc_info()[2].tb_lineno, e))

    async def download_task(self, *, headers={}):
        timeout = aiohttp.ClientTimeout(total=self.timeout_, connect=60)
        
        connector = ProxyConnector.from_url('socks5://127.0.0.1:1080')
        async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
            while not self.tasks.empty():
                key = self.tasks.get()
                retry = self.retry_time
                while retry > 0:
                    try:
                        await self.download_task_rang(session, self.result['task'][key], headers=headers)
                        break
                    except aiohttp.ServerTimeoutError as e:
                        logging.error('[line: %s]' % e)
                        logging.error('[Timeout] %s remain: %s' % (
                            self.result['task'][key]['name'], retry - 1))
                    except aiohttp.ClientResponseError as e:
                        logging.error('[line: %s]' % sys.exc_info()[2].tb_lineno)
                        logging.error('[ResponseError: %s] status: %s, message: %s' % (task['name'], e.status, e.message))
                    except aiohttp.ClientError as e:
                        logging.error('[line: %s]: %s' % (sys.exc_info()[2].tb_lineno, e))
                        # result['task'][key]['complete'] = 2
                        # break
                    except KeyboardInterrupt as e:
                        print('')
                        logging.error(
                            '[%s]KeyboardInterrupt: %s, exit' % (key, e))
                        self.result['task'][key]['complete'] = -1
                        raise e
                        break
                    except BaseException as e:
                        logging.error('[line: %s]' % sys.exc_info()[2].tb_lineno)
                        logging.error('[retry] failed to get %s: %s, remain: %s' % (
                            self.result['task'][key]['name'], e, retry - 1))
                    retry -= 1
                if retry <= 0:
                    self.result['task'][key]['complete'] = 2
                self.result['task'][key]['run'] = False

    async def download_task_rang(self, session, task, *, headers={}, chunk_size=1024):
        if task['complete'] > 0:
            return
        url = task['url']
        filename = task['name']
        if 'range' in task:
            headers['Range'] = 'bytes=%d-%d' % (task['range'][0] + task['size'], task['range'][1])
        try:
            async with session.get(url, headers=headers) as resp:
                if resp.status in (206, 200):
                    curre_size = task['size']
                    if resp.status == 206:
                        total_size = task['range'][1] - task['range'][0]
                    if resp.status == 200:
                        total_size = int(resp.headers.get('Content-Length', 0))
                    if not os.path.exists(filename):
                        fp = open(filename, "wb")
                        fp.truncate(total_size + 1)
                        fp.close()
                    with open(filename, "r+b") as fp:
                        fp.seek(curre_size, 0)
                        while True:
                            chunk = await resp.content.read(chunk_size)
                            if not chunk:
                                break
                            fp.write(chunk)
                            curre_size += len(chunk)
                            task['scale'] = curre_size / (total_size if total_size > 0 else curre_size)
                            task['size'] = curre_size
                    task['complete'] = 1
                    task['scale'] = 1.00
                else:
                    err = "[Error] status: %s, reason" % (
                        resp.status, resp.reason)
                    logging.warning(err)
                    task['err'] = err
                    task['complete'] = -2
        except aiohttp.ClientResponseError as e:
            logging.error('[line: %s]' % sys.exc_info()[2].tb_lineno)
            logging.error('[ResponseError: %s] status: %s, message: %s' % (task['name'], e.status, e.message))
            raise e
        except BaseException as e:
            if self.loop.is_closed(): return
            logging.error('[line: %s]' % sys.exc_info()[2].tb_lineno)
            logging.error('[Error] failed to get %s: %s' % (task['name'], e))
            task['err'] = '[Error] %s' % e
            raise e

    def task_load(self, filename):
        status_file = '%s.json' % filename
        data = None
        if os.path.exists(status_file):
            data = loaddata(status_file)
        if data and len(data.get('task', {})) > 0:
            for key, item in data['task'].items():
                self.result['task'][key] = item
                self.tasks.put(key)

    def task_down(self, filename):
        tasks = [self.download_task(headers=add_header(text=self.is_text)) for index in range(self.thread_num)]
        tasks.append(self.download_status(filename))
        self.loop = asyncio.new_event_loop()
        # print(dir(self.loop))
        # exit(-1)
        try:
            self.loop.run_until_complete(asyncio.wait(tasks))
        except KeyboardInterrupt as e:
            logging.warning('[Stop]')
            for task in asyncio.Task.all_tasks():
                task.cancel()
            self.loop.run_until_complete(asyncio.sleep(0))
            self.loop.close()
            raise e
        for task in asyncio.Task.all_tasks():
            task.cancel()
        self.loop.run_until_complete(asyncio.sleep(0))
        self.loop.close()

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
        dumpdata('%s.json' % filename, self.result)
        if len(complete) != len(self.result['task']):
            logging.warning('Failed to download [%s]: %s/%s' % (filename, len(complete), len(self.result['task'])))
            return (False, None)
        return (True, complete)

    def task_merge(self, filename, complete = [], *, rmts=False):
        # 成功的结果
        if len(complete) <= 0: raise BaseException('number of complete file is 0: %s' % complete)
        root, name_ = filename.rsplit('/', 1)
        keys = {}
        for item in complete:
            key_dir = item['name'].rsplit('/', 1)[0]
            if keys.get(key_dir, None):
                keys[key_dir].append((item['name'], item.get('key', None)))
            else:
                keys[key_dir] = [(item['name'], item.get('key', None))]
        for key, items in keys.items():
            name = '%s/%s' % (key, name_)
            if os.path.exists(name): os.remove(name)
            logging.info('[-]output file: %s' % name)
            with open(name, 'ab') as dst:
                for index, item in enumerate(items, start=1):
                    if not os.path.exists(item[0]): continue
                    with open(item[0], 'rb') as src:
                        if item[1]:
                            # 解密
                            cryptor = AES.new(item[1].encode(), AES.MODE_CBC, item[1].encode())
                            dst.write(cryptor.decrypt(src.read()))
                        else:
                            dst.write(src.read())
                        if rmts:
                            os.remove(item[0])
                    status_str = '%s | (%s / %s)' % (str(item), index, len(items))
                    if self.verbose:
                        print('merge_status: %s%s' % (status_str, ' ' * (100 - len(status_str))), end='\r')
                    dumpdata('%s.status_merge' % name, status_str)
            if self.verbose:
                print('\n[-]output file: %s' % name)

    def download_file_range(self, url, filename, *, blocks=512):
        self.task_load(filename)
        if self.tasks.empty():
            os.makedirs(filename.rsplit('/', 1)[0], exist_ok = True)
            total, mt = get_resource_size(url)
            if not mt: 
                self.thread_num = 1
                blocks = 1
            logging.info('[+]total: %s, %d ts, thread num: %s' %
                        (byteunit(total), blocks, self.thread_num))
            part = total // blocks
            for index in range(blocks):
                name = '%s-%s' % (filename, index)
                task_index = {'name': name, 'url': url, 'range': (part * index + 1 if index > 0 else part * index, total if index == blocks - 1 else part * index + part), 'scale': 0, 'size': 0, 'run': True, 'complete': 0, 'error': None}
                self.tasks.put(name)
                self.result['task'][name] = task_index
        while True:
            self.task_down(filename)
            status, complete = self.task_check(filename)
            if (status):
                self.task_merge(filename, complete, rmts=True)
                break
            self.task_load(filename)

    def download_m3u8(self, url, filename, *, desc={}):
        self.task_load(filename)
        if self.tasks.empty():
            self.download_m3u8_load(url, filename, desc=desc)
        self.task_down(filename)
        status, complete = self.task_check(filename)
        if not status:
            logging.warning('download not complete')
        if filename.endswith('.m3u8'):
            filename = filename.rsplit('.', 1)[0]
        self.task_merge(filename, complete)

    def download_m3u8_load(self, url, filename, *, desc={}):
        os.makedirs(filename.rsplit('/', 1)[0], exist_ok = True)
        save_file(url, filename)
        if not os.path.exists(filename):
            raise BaseException("m3u8 file not exists: %s" % filename)
        content = ''
        file_line = None
        with open(filename, 'r') as src:
            content = src.read()
        if len(content) <= 0:
            raise BaseException("Failed to download m3u8 file: \n%s" % content)
        if '\r\n' in content:
            file_line = content.split("\r\n")
        else:
            file_line = content.split("\n")
        if file_line[0] != "#EXTM3U":
            raise BaseException("it is not m3u8 file: \n%s" % content)
        tss = []
        duration = 0.0
        key = None
        with open(filename, 'w') as src:
            url_root = '%s%s' % (url[:url.index('://')+3], url[url.index('://')+3:].split('/', 1)[0])
            uri = '/%s' % url[url.index('://')+3:].split('/', 1)[1]
            for line in file_line:
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
                    save_file(key_url, key_path)
                    with open(key_path, 'r') as key_src:
                        key = key_src.read()
                    line = '%sURI="%s"' % (line[:line.index('URI=')], key_uri if '/' not in key_uri else key_uri.rsplit('/', 1)[1])
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
                if line.startswith('http'):
                    line = '/%s' % line[line.index('://') + 3:].split('/', 1)[1]
                    line_ = line.split('/')
                    uri_ = uri.split('/')
                    index = 0
                    while (index < min(len(line_), len(uri_))) and line_[index] == uri_[index]:
                        index += 1
                    line = '/'.join(line_[index:])
                    line__ = line
                src.write('%s\n' % line)
                if "#EXT" in line or len(line.strip()) == 0: continue
                if line__:
                    tss.append((line__, '%s/%s' % (filename.rsplit('/', 1)[0], line)))
                else:
                    tss.append(('%s/%s' % (url.rsplit('/', 1)[0], line),'%s/%s' % (filename.rsplit('/', 1)[0], line)))
        desc['duration'] = duration
        for url, name in tss:
            if resource_name(url).endswith('.m3u8'):
                self.download_m3u8_load(url, name, desc=desc)
            else:
                self.result['task'][name]={'name': name, 'url': url, 'scale': 0, 'size': 0, 'run': True, 'complete': 0, 'error': None, 'key': key}
                self.tasks.put(name)
