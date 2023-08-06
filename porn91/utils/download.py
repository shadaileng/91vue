#!/usr/bin/python3
# -*- coding: utf-8 -*-

from urllib import request
from urllib.error import URLError

import random, asyncio, re, os, sys, time, json, logging, time
import socket
import queue
from functools import reduce

import requests
import aiohttp
from Crypto.Cipher import AES

def getCols():
    cols = 100
    try:
        import subprocess
        cols = int(subprocess.Popen(['tput','cols'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0])
    except BaseException as e:
        logging.error('[-]Error: %s' % e)
    return cols

COLS = getCols()

def random_ip():
    a=random.randint(1,255)
    b=random.randint(1,255)
    c=random.randint(1,255)
    d=random.randint(1,255)
    return "%s.%s.%s.%s" % (str(a), str(b), str(c), str(d))

def random_Agent():
    agents = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11",
    "Opera/9.25 (Windows NT 5.1; U; en)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12",
    "Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9",
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
    "'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/83.0.4103.116 Chrome/83.0.4103.116 Safari/537.36'"
    ]
    return random.choice(agents)

def add_header(text=True):
    base = {
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7", 
        "Proxy-Connection": "keep-alive", 
        "User-Agent": random_Agent()
        # ,"X-Forwarded-For":random_ip()
    }
    if not text:
        base["Accept-Encoding"] = "gzip, deflate, br"
    return base

def custom_header(header_str, headers={}):
    flag = '\n'
    if '\r\n' in header_str:
        flag = '\r\n'
    for item in header_str.split(flag):
        key, val = item.split(':', 1)
        if key == 'Accept-Encoding': continue
        headers[key]=val.strip()
    
def get_cookie(cookie_str):
    items = cookie_str.split(';')
    cookies = {}
    for item in items:
        key, val = item.strip().split('=', 1)
        cookies[key]=val
    return cookies


def resource_name(url):
    url = url.split('?', 1)[0] if '?' in url else url
    url = url.split('&', 1)[0] if '&' in url else url
    return url.rsplit('/', 1)[1] if '/' in url else url

def wget(url, headers={}):
    buf = {'status': False, 'msg': ''}
    try:
        req = request.Request(url)
        for key, val in add_header().items():
            req.add_header(key, val)
        for key, val in headers.items():
            req.add_header(key, val)
        with request.urlopen(req) as resp:
            if resp.status == 200:
                buf = {'status': True, 'msg': resp.read().decode("utf-8", errors='ignore')}
            else:
                buf = {'status': False, 'msg': 'status: %s, reason: %s' % (resp.status, resp.reason)}
    except URLError as e:
        logging.error('[-]URLError[%s]: %s' % (sys.exc_info()[2].tb_lineno, e))
        buf = {'status': False, 'msg': e}
    except BaseException as e:
        logging.error('[-]Error[%s]: %s' % (sys.exc_info()[2].tb_lineno, e))
        buf = {'status': False, 'msg': e}
    return buf

def save_file(url, name, headers={}):
    logging.info('[-]wget %s' % url)
    result = wget(url, headers)
    if result['status']:
        with open(name, 'w') as dst:
            dst.write(result['msg'])
        return
    raise BaseException('[-] failed to get [%s]: %s' % (url, result['msg']))

def byteunit(byte):
    return '%.2fKB' % (byte / 1024.0) if byte / 1024.0 < 1024 else ('%.2fMB' % (byte / 1024.0 / 1024.0) if (byte / 1024.0 / 1024.0) < 1024 else '%.2fGB' % (byte / 1024.0 / 1024.0 / 1024.0))

def loaddata(filename):
    try:
        tmp_buf = ''
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as dst:
                tmp_buf = dst.read()
            if tmp_buf and len(tmp_buf) > 0:
                return json.loads(tmp_buf)
                # return json.loads(tmp_buf, encoding='utf-8')
        else:
            raise BaseException('file %s not exists' % filename)
    except BaseException as e:
        logging.warning('[-]Error[%s]: %s' % (sys.exc_info()[2].tb_lineno, e))
    return None

def dumpdata(filename, data):
    try:
        with open(filename, 'w') as dst:
            if isinstance(data, str):
                dst.write(data)
            else:
                dst.write(json.dumps(data, ensure_ascii=False))
        return True
    except BaseException as e:
        logging.error('[-]Error[%s]: %s' % (sys.exc_info()[2].tb_lineno, e))
        if isinstance(e, KeyboardInterrupt): raise e
    return False

def get_resource_size(url):
    '''
    获取资源大小
    '''
    '''
    req = request.Request(url)
    for key, value in add_header().items():
        req.add_header(key, value)
    req.add_header('Range', 'bytes=0-4')
    with request.urlopen(req) as resp:
        pass
    '''
    total = 0
    mt = False
    headers = add_header()
    logging.info('[-]wget %s' % url)
    resp = requests.head(url, headers=headers)
    # resp.status_code, resp.reason
    headers = resp.headers
    if resp.status_code == 206:
        rex = re.match(r'^bytes 0-4/(\d+)$', headers['Content-Range'])
        if rex:
            total = int(rex.group(1))
            mt = True
    elif resp.status_code == 200:
        total = int(headers['Content-Length'])
        num_thread = 1
    else:
        raise BaseException('status: %s, reason: %s' % (resp.status_code, resp.reason))
    if total <= 0: raise BaseException('total is Zero')
    return total

async def download_rang_task(task, chunk_size=1024, timeout_ = 240, text = False, mt = True, show=True):
    if task['complete'] > 0: return
    task['run'] = True
    headers = add_header(text)
    filename = task['name']
    if 'range' in task:
        headers['Range'] = 'bytes=%d-%d' % (task['range'][0] + task['size'], task['range'][1])
    if show:
        if 'range' in task:
            logging.info('[%s]wget [%s]: Range(%d-%d)' % (filename, task['url'], task['range'][0] + task['size'], task['range'][1]))
        else:
            logging.info('[%s]wget [%s]' % (filename, task['url']))
    timeout = aiohttp.ClientTimeout(total=timeout_, connect=60)
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(task['url'], headers=headers) as resp:
                # 206 | 200 分开
                if resp.status in (206, 200):
                    if resp.status == 206:
                        total_size = task['range'][1] - task['range'][0]
                        curre_size = task['size']
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
                    if resp.status == 200:
                        total_size = int(resp.headers.get('Content-Length', 0))
                        curre_size = task['size']
                        with open(filename, "wb") as fp:
                            while True:
                                chunk = await resp.content.read(chunk_size)
                                if not chunk:
                                    break
                                fp.write(chunk)
                                curre_size += len(chunk)
                                task['scale'] = curre_size / (total_size if total_size > 0 else curre_size)
                                task['size'] = curre_size
                    task['scale'] = 1
                    task['run'] = False
                    task['complete'] = 1
                else:
                    if resp.status >= 500 or resp.status in [403, 404, 416]:
                        task['complete'] = 2
                        logging.error('[-]status: %s, reason: %s' % (resp.status, resp.reason))
                    else:
                        task['complete'] = -1
                    task['run'] = False
                    raise BaseException('status: %s, reason: %s' % (resp.status, resp.reason))
    except BaseException as e:
        if task['complete'] != 2:
            task['complete'] = -1
            task['run'] = False
        logging.error('[%s]Error line [%s]: %s' % (task['name'], sys.exc_info()[2].tb_lineno, e))
        raise e

async def download_task(tasks, result={'_status': True, 'task': {}}, retries=50, text=False):
    try:
        while not tasks.empty():
            key = tasks.get()
            retry = retries
            while retry > 0:
                try:
                    await download_rang_task(result['task'][key], text=text)
                    result['task'][key]['complete'] = 1
                    result['task'][key]['run'] = False
                    break
                except asyncio.TimeoutError as e:
                    logging.error('[%s]TimeoutError: %s, remain: %s' % (key, e, retry - 1))
                    result['task'][key]['complete'] = -1
#                except aiohttp.ClientError as e:
#                    logging.error('[%s]ClientError: %s, exit' % (key, e))
#                    result['task'][key]['complete'] = 2
#                    break
                except KeyboardInterrupt as e:
                    logging.error('[%s]KeyboardInterrupt: %s, exit' % (key, e))
                    result['task'][key]['complete'] = -1
                    break
                except BaseException as e:
                    result['task'][key]['run'] = False
                    if result['task'][key]['complete'] == 2:
                        logging.error('[%s]Error line [%s]: %s' % (key, sys.exc_info()[2].tb_lineno, e))
                        break
                    logging.error('[%s]Error: %s, remain: %s' % (key, e, retry - 1))
                retry -= 1
            if retry <= 0:
                result['task'][key]['complete'] = 2
    except BaseException as e:
        logging.error('[-]Error[%s]: %s' % (sys.exc_info()[2].tb_lineno, e))

async def task_status(result, filename, show=True, speed={'beg_t': 0, 'beg_d': 0, 'dtl': 0}, loop=None):
    tmp_file = '%s.json' % filename
    logging.info('[-]output file: %s' % tmp_file)
    dumpdata(tmp_file, result)
    while True:
        # 结束任务
        tmp_result = loaddata(tmp_file)
        if not tmp_result.get('_status', True) and loop:
            logging.warning('[Stoping]')
            loop.stop()
            loop.run_forever()
            logging.warning('[Stoped]')
            break
        dumpdata(tmp_file, result)
        flag = True
        status_str = ''
        sum = 0.0
        total = 0
        thread_num = 0
        if len(result.get('task', {})) > 0:
            for key, item in result['task'].items():
                if key == '_status': continue
                sum += float(item.get('scale') * 100)
                total += item.get('size')
                if item['complete'] == 0 or item['complete'] == -1: flag = False
                if item['run']: thread_num += 1
            cur = time.time()
            if speed['beg_t'] == 0:
                speed['beg_d'] = total
                speed['beg_t'] = cur
                
            if cur - speed['beg_t'] >= 1:
                speed['dtl'] = (total - speed['beg_d']) / (cur - speed['beg_t'])
                speed['beg_d'] = total
                speed['beg_t'] = cur
            status_str = '%s(%.2f%%, %s/s) | %d' % (byteunit(total), sum / len(result.get('task', {})), byteunit(speed['dtl']), thread_num)
        else:
            status_str = '[Error] task of result is empty: %s' % result
        if show:
            print('status: %s%s' % (status_str, ' ' * (0 if len(status_str) > COLS - 10 else COLS - len(status_str) - 10)), end='\r')
        dumpdata('%s.status' % filename, status_str)
        if flag: break
        await asyncio.sleep(0.1)
    speed={'beg_t': 0, 'beg_d': 0, 'dtl': 0}
    logging.info('\ndownload complete')

def merge_task(complete, filename, *, show=True, rmts=True):
    if len(complete) <= 0: raise BaseException('number of complete file is 0: %s' % complete)
    root, name = filename.rsplit('/', 1)
    keys = {}
    for item in complete:
        key_dir = item['name'].rsplit('/', 1)[0]
        if keys.get(key_dir, None):
            keys[key_dir].append((item['name'], item.get('key', None)))
        else:
            keys[key_dir] = [(item['name'], item.get('key', None))]
    for key, items in keys.items():
        name = '%s/%s' % (key, name)
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
                if show:
                    print('status: %s%s' % (status_str, ' ' * (100 - len(status_str))), end='\r')
                dumpdata('%s.status_merge' % name, status_str)

def download_create(filename, task = queue.Queue(-1), result={'_status': True, 'task': {}}, *, show=True, num_thread=128, rmts=True, text=False, desc={}):
    data = None
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    file_data = '%s.json' % filename
    if os.path.exists(file_data):
        data = loaddata(file_data)
        if data and len(data.get('task', {})) > 0:
            task = queue.Queue(-1)
            for key, item in data['task'].items():
                result['task'][key] = item
                task.put(key)
    if task.qsize() <= 0: raise BaseException('task is empty: %s' % task.qsize())
    if len(result) <= 0: raise BaseException('result is empty: %s' % result)
    result['_status'] = True
    tasks = [download_task(task, result, text=text) for index in range(num_thread)]
    speed={'beg_t': 0, 'beg_d': 0, 'dtl': 0}
    tasks.append(task_status(result, filename, show, speed, loop))
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

def download_file(url, filename, *, num_thread=128, blocks = 128, desc={}, show=True):
    task = queue.Queue(-1)
    result={'_status': True, 'task': {}}

    total = get_resource_size(url)
    logging.info('[+]total: %s, %d ts, thread num: %s' % (byteunit(total), blocks, num_thread))
    part = total // blocks
    for index in range(blocks):
        name = '%s-%s' % (filename, index)
        task_index = {'name': name, 'url': url, 'range': (part * index + 1 if index > 0 else part * index, total if index == blocks - 1 else part * index + part), 'scale': 0, 'size': 0, 'run': False, 'complete': 0, 'error': None}
        task.put(name)
        result['task'][name] = task_index

    start_t = time.time()
    download_create(filename, task, result, num_thread=128, desc=desc, show=show)
    
    desc['status'] = result['_status']
    if not result['_status']:
        logging.info('\n[-]Stop')
        raise BaseException('[-]Stop')
    # 成功的结果
    complete = []
    for key, item in result['task'].items():
        if item['complete'] == 1:
            if os.path.exists(key):
                complete.append(item)
            else:
                result['task'][key]['complete'] = -1
                result['task'][key]['size'] = 0
    dumpdata('%s.json' % filename, result)
    # complete = [item for key, item in result['task'].items() if item['complete'] == 1 and os.path.exists(key)]
    
    if len(complete) != blocks:
        raise BaseException('Failed to download [%s]: %s/%s' % (filename, len(complete), blocks))
    # 合并
    merge_task(complete, filename, show=show)
    size = reduce(lambda x, y: x + y, [item['size'] for item in complete])
    desc['size'] = size
    '''
    file_data_ = ''
    if '/' in filename:
        file_data_ = '%s/.%s.json' % tuple(filename.rsplit('/', 1))
    else:
        file_data_ = '.%s.json' % filename
    if os.path.exists(file_data_): os.remove(file_data_)
    os.rename(file_data, file_data_)
    '''
    logging.info('\n[-]SUCCESS')
    logging.info('[-]spend: %ds' % int(time.time() - start_t))

def download_multifile(tasks, root_path, *, num_thread=3, desc={}, show=True):
    task = queue.Queue(-1)
    result={'_status': True, 'task': {}}
    for url, name in tasks:
        result['task'][name] = {'name': name, 'url': url, 'scale': 0, 'size': 0, 'run': False, 'complete': 0, 'error': None}
        task.put(name)
    start_t = time.time()
    download_create('%s/%s' % (root_path, time.time()), task, result, num_thread=num_thread, text=True, show=show)
    logging.info('\n[-]SUCCESS')
    logging.info('[-]spend: %ds' % int(time.time() - start_t))

def download_m3u8(url, filename, * , num_thread=128, desc = {}, show=True):
    result={'_status': True, 'task': {}}
    task = queue.Queue(-1)
    download_m3u8_load(url, filename, result, task, desc)
    # print(result, desc)
    start_t = time.time()
    download_create('%s.mp4' % filename.rsplit('.', 1)[0], task, result, num_thread=128, desc=desc, show=show)
    
    desc['status'] = result['_status']
    if not result['_status']:
        logging.info('\n[-]Stop')
        return
    # 成功的结果
    complete = [item for key, item in result['task'].items() if item['complete'] == 1 and os.path.exists(key)]
    
    # 合并
    merge_task(complete, filename, rmts=False, show=show)
    size = reduce(lambda x, y: x + y, [item['size'] for item in complete])
    desc['size'] = size
    '''
    file_data_ = ''
    if '/' in filename:
        file_data_ = '%s/.%s.json' % tuple(filename.rsplit('/', 1))
    else:
        file_data_ = '.%s.json' % filename
    if os.path.exists(file_data_): os.remove(file_data_)
    os.rename(file_data, file_data_)
    '''
    logging.info('\n[-]SUCCESS')
    logging.info('[-]spend: %ds' % int(time.time() - start_t))
    
def download_m3u8_load(url, filename, result={'_status': True, 'task': {}}, task = queue.Queue(-1), desc={}):
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
            download_m3u8_load(url, name, result, task, desc)
        else:
            result['task'][name]={'name': name, 'url': url, 'range': (1, 1), 'scale': 0, 'size': 0, 'run': False, 'complete': 0, 'error': None, 'key': key}
            task.put(name)

async def download_range(url, filename, index, result={}, range_ = (0, 0), params={}, chunk_size=1024, timeout_ = 60, text = False, mt = True, retries=30):
    exception_ = None
    clear = False
    while retries > 0:
        try:
            if not result[index]['run']:
                return
            headers = add_header(text)
            if mt:
                headers['Range'] = 'bytes=%d-%d' % (range_[0] + result[index]['size'], range_[1])
            logging.info('[%s]wget [%s]' % (index, url))
            timeout = aiohttp.ClientTimeout(total=timeout_)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url, headers=headers) as resp:
                    if resp.status == 206 or resp.status == 200:
                        total_size = range_[1] - range_[0]
                        curre_size = result[index]['size']
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
                                result[index]['scale'] = curre_size / (total_size if total_size > 0 else curre_size)
                                result[index]['size'] = curre_size
                        result[index] = {'scale': 1, 'size': curre_size, 'run': False, 'error': None}
                    else:
                        raise BaseException('status: %s, reason: %s' % (resp.status, resp.reason))
            return
        except BaseException as e:
            logging.error('[%s] Error[%s]: %s, remain: %s' % (index, sys.exc_info()[2].tb_lineno, e, retries - 1))
            exception_ = e
            retries -= 1
    result[index]['run'] = False
    result[index]['error'] = exception_
    raise BaseException('[-]task-%s cause error: %s' % (index, exception_))

async def status(result, filename, show=True):
    tmp_file = '%s.json' % filename
    logging.info('[-]output file: %s' % tmp_file)
    with open(tmp_file, 'w') as dst:
        dst.write(json.dumps(result, ensure_ascii=False))
    while True:
        with open(tmp_file, 'w') as dst:
            dst.write(json.dumps(result, ensure_ascii=False))
        flag = True
        status_str = ''
        for index in range(len(result)):
            cur_status = result.get(str(index))
            if cur_status.get('run'): flag = False
            status_str += '%s(%.2f%%)%s| ' % (byteunit(cur_status.get('size')), float(cur_status.get('scale') * 100), 'o' if cur_status.get('run') else 'x')
        if show:
            print('status: %s%s' % (status_str, ' ' * (100 - len(status_str))), end='\r')
        if flag: break
        await asyncio.sleep(0.1)
    print('')

def download(url, filename, num_thread=5):
    # 恢复备份的socket
    # if socket_bak: socket.socket = socket_bak
    start_t = time.time()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        total = get_resource_size(url)
        logging.info('[+]total: %s, thread num: %s' % (byteunit(total), num_thread))
        part = total // num_thread
        file_data = '%s.json' % filename
        file_data_ = ''
        if '/' in filename:
            file_data_ = '%s/.%s.json' % tuple(filename.rsplit('/', 1))
        else:
            file_data_ = '.%s.json' % filename
        result = loaddata(file_data)
        if not result:
            result = {}
            for i in range(num_thread):
                result[str(i)] = {'scale': 0, 'size': 0, 'run': True, 'error': None}
        tasks = [download_range(url, '%s-%s' % (filename, index), str(index), result, (part * index + 1 if index > 0 else part * index, total if index == num_thread - 1 else part * index + part)) for index in range(num_thread)]
        tasks.append(status(result, filename))
        loop.run_until_complete(asyncio.wait(tasks))
        for index in range(num_thread):
            if result[str(index)]['error']: 
                raise BaseException('[-]task-%s cause error: %s' % (index, result[index]['error']))
            src_path = '%s-%s' % (filename, index)
            if not os.path.exists(src_path):
                raise BaseException('[-]tmp filename %s not exists' % src_path)
        if os.path.exists(filename): os.remove(filename)
        with open(filename, 'ab') as dst:
            for index in range(num_thread):
                src_path = '%s-%s' % (filename, index)
                if os.path.exists(src_path):
                    with open(src_path, 'rb') as src:
                        dst.write(src.read())
                        os.remove(src_path)
        if os.path.exists(file_data_): os.remove(file_data_)
        os.rename(file_data, file_data_)
        loop.close()
    except KeyboardInterrupt as e:
        loop.stop()
        logging.error('[-]Stop[%s]: %s' % (sys.exc_info()[2].tb_lineno, e))
    except URLError as e:
        logging.error('[-]URLError[%s]: %s' % (sys.exc_info()[2].tb_lineno, e))
    except BaseException as e:
        logging.error('[-]Error[%s]: %s' % (sys.exc_info()[2].tb_lineno, e))
    logging.info('[-]spend: %ds' % int(time.time() - start_t))
    logging.info('SUCCESS')

def download_(url, filename, num_thread=128, blocks = 128):
    # 恢复备份的socket
    # if socket_bak: socket.socket = socket_bak
    start_t = time.time()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    task = queue.Queue(-1)
    result = {}
    data = None
    file_data = '%s.json' % filename
    file_data_ = ''
    if '/' in filename:
        file_data_ = '%s/.%s.json' % tuple(filename.rsplit('/', 1))
    else:
        file_data_ = '.%s.json' % filename
    if os.path.exists(file_data):
        data = loaddata(file_data)
        for key, item in data.items():
            task.put(key)
            result[key] = item
    if not data:
        total = get_resource_size(url)
        print('[+]total: %s, %d ts, thread num: %s' % (byteunit(total), blocks, num_thread))
        part = total // blocks
        for index in range(blocks):
            name = '%s-%s' % (filename, index)
            task_index = {'name': name, 'url': url, 'range': (part * index + 1 if index > 0 else part * index, total if index == blocks - 1 else part * index + part), 'scale': 0, 'size': 0, 'run': False, 'complete': 0, 'error': None}
            task.put(name)
            result[name] = task_index
    
    tasks = [download_task(task, result) for index in range(num_thread)]
    tasks.append(task_status(result, filename))
    loop.run_until_complete(asyncio.wait(tasks))
    complete = [key for key, item in result.items() if item['complete'] == 1 and os.path.exists(key)]
    if len(complete) <= 0: raise BaseException('number of complete file is 0: %s' % complete)
    if os.path.exists(filename): os.remove(filename)
    with open(filename, 'ab') as dst:
        for key in complete:
            if os.path.exists(key):
                with open(key, 'rb') as src:
                    dst.write(src.read())
                    os.remove(key)
    if os.path.exists(file_data_): os.remove(file_data_)
    os.rename(file_data, file_data_)
    loop.close()
    print('[-]SUCCESS')
    print('[-]spend: %ds' % int(time.time() - start_t))
    return True
    
async def task_01(tasks, result={}, retries=30):
    try:
        while not tasks.empty():
            task = tasks.get()
            key = task['name']
            while retries > 0:
                try:
                    # print(task)
                    result[key] = task
                    await asyncio.sleep(0.1 * task['value'])
                    if retries > 29: raise BaseException('retry')
                    result[key]['complete'] = 1
                    break
                except BaseException as e:
                    print('[%s]Error: %s, remain: %s' % (task['name'], e, retries - 1))
                    retries -= 1
                result[key]['complete'] = -1
            retries=30
    except BaseException as e:
        print('[-]Error[%s]: %s' % (sys.exc_info()[2].tb_lineno, e))

def download__(url, filename, num_thread=5):
    # 恢复备份的socket
    # if socket_bak: socket.socket = socket_bak
    start_t = time.time()
    try:
        total = 100
        print('[+]total: %s, thread num: %s' % (byteunit(total), num_thread))
        part = total // num_thread
        task = queue.Queue(-1)
        result = {}
        
        for index in range(10):
            task.put({'name': '%s-%s' % (filename, index), 'value': index})
        print(task.qsize())
        tasks = [task_01(task, result) for index in range(num_thread)]
        # tasks.append(task_status(result, filename))
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(asyncio.wait(tasks))
        print(result)
        loop.close()
        print('[-]SUCCESS')
    except KeyboardInterrupt as e:
        loop.stop()
        print('\n[-]Stop[%s]: %s' % (sys.exc_info()[2].tb_lineno, e))
    except BaseException as e:
        print('\n[-]Error[%s]: %s' % (sys.exc_info()[2].tb_lineno, e))
    print('[-]spend: %ds' % int(time.time() - start_t))
