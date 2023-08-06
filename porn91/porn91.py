#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import re
import time
import logging
import threading
import js2py

from datetime import datetime
from bs4 import BeautifulSoup

from main import loaddatadb, dumpdatadb
from utils.daemon import CDaemon
from utils import arg_list
from aioweb.logger import set_logger

from aioweb import settings
from main import get_config, load_items
from download import download_file_range, download_file_mulity, download_m3u8
from download import resource_name
from aioweb import corelib

# baseurl = 'http://www.91porn.com/view_video.php?viewkey=%s'
# baseurl = 'http://91porn.com/view_video.php?viewkey=%s&page=&viewtype=basic&category='
baseurl = 'http://www.91porn.com'
settings.config_init()
base_dir = settings.config['base_dir']
pagedir = '%s/pages' % base_dir
videodir = '%s/video' % base_dir
posterdir = '%s/poster' % base_dir
m3u8dir = '%s/m3u8' % base_dir
data_path = '%s/data.db' % base_dir
jsdir = '%s/js' % base_dir
md5url = 'http://91porn.com/js/md5.js'
md5 = '%s/md5.js' % jsdir
socket_bak = None

os.makedirs(pagedir, exist_ok=True)
os.makedirs(videodir, exist_ok=True)
os.makedirs(posterdir, exist_ok=True)
os.makedirs(m3u8dir, exist_ok=True)
os.makedirs(jsdir, exist_ok=True)


def save_file(url, filename, desc={}, *, verbose=False, blocks=512):
    headers = {}
    headers = {'Cookie': get_config('91cookie', '')}
    # proxy = get_config('proxy', 'socks5://127.0.0.1:1080')
    proxy = get_config('proxy')
    if ".m3u8" not in url:
        return download_file_range(url, filename, desc=desc, blocks=blocks, verbose=verbose, proxy=proxy, headers=headers)
    else:
        return download_m3u8(url, filename, desc=desc, blocks=blocks, verbose=verbose, proxy=proxy, headers=headers)


def download_multifile(tasks=[], *, verbose=False, **kw):
    headers = {'Cookie': get_config('91cookie', '')}
    proxy = get_config('proxy')
    download_file_mulity(tasks, verbose=verbose, proxy=proxy, headers=headers)


def get_parse_source(key):
    data = {}
    content = ''
    filename = f'{pagedir}/{key}.html'
    if not os.path.exists(filename):
        logging.warning(f'[-]{filename} not exists')
        return data
    with open(filename, 'r', encoding="utf-8" ) as dst:
        content = dst.read()
    # s(content)
    soup = BeautifulSoup(content, features='html.parser')
    dom_name = soup.select_one('.login_register_header')
    logging.info(f'dom_name: {dom_name.get_text()}')

    if dom_name:
        name_ = dom_name.text
        if len(name_) > 0:
            data['name'] = name_.strip()
        else:
            name_ = str(dom_name.select("img")[-1])
            if name_:
                data['name'] = name_.strip()
    else:
        logging.warning('视频不存在,可能已经被删除或者被举报为不良内容!')

    #################.title-yakov##############
    logging.info(soup.select('.title-yakov'))
    dom_user = soup.select('.title-yakov')[-1]
    if dom_user and dom_user.find('a'):
        dom_user.find('a')['href']
        data['uid'] = re.search('UID=(.+)', dom_user.find('a')['href']).group(1)
        uname_dom = dom_user.select_one('span.title')
        if uname_dom and uname_dom.contents and len(uname_dom.contents) > 0:
            data['uname'] = str(uname_dom.contents[0])
        else:
            data['uname'] = str(uname_dom)
    else:
        data['uid'] = ''
        data['uname'] = '匿名'
    ##################video##################
    logging.info(soup.select_one('video'))
    dom_video = soup.select_one('video')
    if dom_video:
        data['poster'] = dom_video['poster']
        dome_source = dom_video.select_one('source')
        if dome_source:
            data['src'] = dome_source['src']
        else:
            # 加密的视频链接
            context = md5_Ctx()
            if context is None:
                logging.warning(f'[-]md5_Ctx Failed')
                return data
            src = context.eval(query_doc_write(dom_video))
            logging.info(src)
            if src:
                dome_source = BeautifulSoup(src, features='html.parser')
                if dome_source.source:
                    data['src'] = dome_source.source.get('src', None)
    else:
        logging.warning("游客")
    baseurl = get_config('baseurl', 'http://www.91porn.com')
    data['url'] = f'{baseurl}/view_video.php?viewkey={key}'

    ##############publish_date_dom##############
    publish_date_dom = soup.find("span", string=re.compile("\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12][0-9]|3[01])"))
    if publish_date_dom:
        data['publish_date'] = publish_date_dom.string.replace('-', '')
    return data

def query_doc_write(dom_doc_write):
    logging.info(f'dom: {dom_doc_write}')
    dom_referer = dom_doc_write.find(string=re.compile("document.write\("))
    if not dom_referer:
        logging.warning('not found document.write\(')
        return
    group = re.search('document.write\((.+)\);', dom_referer.string)
    if not group:
        logging.warning('failed to parse document.write\((.+)\);')
        return
    src = re.search('document.write\((.+)\);', dom_referer.string).group(1)
    return src

def get_url(key):
    baseurl = get_config('baseurl', 'http://www.91porn.com')
    baseurl = f'{baseurl}/view_video.php?viewkey={key}'
    path = f'{pagedir}/{key}.html'
    save_file(baseurl, path, blocks=1)
    return os.path.exists(path)


def import_keys(keys, show=True):
    '''
    异步下载,避免429错误,并发次数3
    '''
    # base_url = 'http://91porn.com/view_video.php?viewkey=%s'
    baseurl = get_config('baseurl', 'http://www.91porn.com')
    base_url = f'{baseurl}/view_video.php?viewkey'
    # baseurl % key, '%s/%s.html' % (pagedir, key)

    # 下载播放页面
    result = {}
    try:
        result_obj = {}
        for key in keys:
            result_obj[key] = {'key': key, 'status': 0}
        dumpdatadb(result_obj, "Porn91")
        tasks = [(f'{base_url}={key}', f'{pagedir}/{key}.html') for key in keys]
        download_multifile(tasks, verbose=show)
    except KeyboardInterrupt as e:
        logging.warning('[-]exit')
        logging.info(f'[-] Stop: {e}')
    except BaseException as e:
        logging.info(f'[-] Stop: {e}')
    result_obj = {}
    for key in keys:
        data = {'key': key, 'status': -1}
        filename = f'{pagedir}/{key}.html'
        if not os.path.exists(filename):
            logger.warning(f"[-]not exists: {filename}")
            data['status'] = -2
        result_obj[key] = data
    dumpdatadb(result_obj, "Porn91")


def update_keys(keys):
    '''
    批量解析播放页面
    '''
    for index, key in enumerate(keys, start=1):
        logging.info(f'[-] task[{key}] {index}/{len(keys)}')
        try:
            item = loaddatadb(key, "Porn91")
            data = {'status': 0}
            dumpdatadb({key: data}, "Porn91")
            result = get_url(key)
            if result:
                data = get_parse_source(key)
                if item.status == 1:
                    data['status'] = 1
                else:
                    data['status'] = -1
            else:
                logging.info(f'[-] Failed to save[{key}]')
                data['status'] = -2
            if not data.get('name', None):
                data['status'] = -2
            if not data.get('src', None):
                data['src'] = ''
                data['status'] = -2
            logging.info(f'[-] dump {key}: {data}')
            dumpdatadb({key: data}, "Porn91")
        except KeyboardInterrupt as e:
            logging.info(f'[-] Stop: {e}')
            dumpdatadb({key: {'status': -1}}, "Porn91")
            return
        # '''
        except BaseException as e:
            logging.error(f'{corelib.printException(e)}-[{key}]ERROR: {e}')
            dumpdatadb({key: {'status': -2}}, "Porn91")
        # '''


def download_keys(keys, show=True):
    result_obj = {}
    for index, key in enumerate(keys, start=1):
        try:
            item = loaddatadb(key, "Porn91")
            # 下载文件
            logging.info(f'[-] task[{key}] {index}/{len(keys)}')
            if not item or not item.src or item.status == 1:
                logging.warning(f'[skip] item[{key}]: {item}')
                continue
            src = item.src
            data = {'status': 0}
            dumpdatadb({key: data}, "Porn91")
            filename = resource_name(src)
            # if ".m3u8" in src:
            #     src_local = '%s/%s' % (m3u8dir, filename)
            #     src_local_base = 'm3u8/%s' % filename
            src_local = f'{videodir}/{filename}'
            data['src_local'] = f'video/{filename.rsplit(".", 1)[0]}.mp4'
            desc = {}
            save_file(src, src_local, desc=desc, verbose=show)
            # print('- * 25')
            # print(desc)
            # print('- * 25')
            data['size'] = desc.get('size', 0)
            data['duration'] = desc.get('duration', 0)
            data['status'] = 1
            src_local_ = f'{videodir}/{filename.rsplit(".", 1)[0]}.mp4'
            if not os.path.exists(src_local_):
                logging.warning(f'[-] src_local not exists: {src_local_}')
                dumpdatadb({key: {'status': -2}}, "Porn91")
                continue
            poster = item.poster
            postername = resource_name(poster)
            poster_local = f'{posterdir}/{postername}'
            data['poster_local'] = f'poster/{postername}'
            save_file(poster, poster_local, verbose=show, blocks=1)
            if not os.path.exists(poster_local):
                logging.warning(f'[-] poster_local not exists: {poster_local}')
            logging.info(f'[-] dump {key}: {data}')
            dumpdatadb({key: data}, "Porn91")
        except KeyboardInterrupt as e:
            logging.info(f'[-] Stop: {e}')
            dumpdatadb({key: {'status': -1}}, "Porn91")
            return
        except BaseException as e:
            logging.error(f'[{key}]ERROR: {e}')
            if "Event loop stopped" in str(e):
                dumpdatadb({key: {'status': -1}}, "Porn91")
                break
            dumpdatadb({key: {'status': -2}}, "Porn91")


def thumbnails_keys(keys, show=True):
    result_obj = {}
    for index, key in enumerate(keys, start=1):
        try:
            logging.info(f'[-] task[{key}] {index}/{len(keys)}')
            item = loaddatadb(key, "Porn91")
            if not item.src_local:
                continue
            # item.src_local, f'{item.src_local.rsplit(".", 1)[0]}.png'

            src = os.path.join(base_dir, item.src_local)
            # print(ffmpeg.probe(src)['streams'])
            duration = thumbnails(src, f'{src.rsplit(".", 1)[0]}.png')
            dumpdatadb({item.key: {'duration': duration}}, "Porn91")
        except BaseException as e:
            logging.error(f'[ERROR]{key}: {repr(e)}')


def thumbnails(src, dst, frames=80):
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
    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = result.communicate()
    if result.returncode != 0:
        logging.error(stderr)
    logging.info(f'[-]output file: {dst}')
    return duration


def load_list(base_url, flag, beg, end, show=True):
    '''
    异步下载,避免429错误,并发次数3
    '''
    keys = [index for index in range(beg, end)]
    rand = datetime.now().strftime('%Y%m%d')
    files = [f'{pagedir}/{flag}-{key}-{rand}.html' for key in keys]
    tasks = [(base_url % key, f'{pagedir}/{flag}-{key}-{rand}.html') for key in keys]
    download_multifile(tasks, verbose=show)
    result_obj = {}
    for filename in files:
        if not os.path.exists(filename):
            logging.warning(f"[-] not exists: {filename}")
            continue
        result_rf = parse_list(filename)
        result_obj = dict(result_obj, **result_rf)
        logging.info(f'[-] Parse Sucess: {filename}')
    return result_obj

def md5_Ctx():
    context = js2py.EvalJs()
    if not os.path.exists(md5):
        md5url = get_config('91md5url', 'http://91porn.com/js/md5.js')
        save_file(md5url, md5, blocks=1)
        if not os.path.exists(md5):
            logging.info(f'[-] Failed to Save: {md5}')
            return None
    js_code = ''
    with open(md5, 'r', errors='ignore') as dst:
        js_code = dst.read()
    js_code = '%s;' % js_code.rsplit(';', 1)[0]
    context.execute(js_code)
    return context

def parse_list(filename, result_obj = {}):
    if not os.path.exists(filename):
        logging.warning(f'[-]not exists: {filename}')
        return result_obj
    content = ''
    with open(filename, 'r', encoding="utf-8", errors='ignore') as dst:
        content = dst.read()
        context = md5_Ctx()
        if context is None:
            logging.warning(f'[-]md5_Ctx Failed')
            return result_obj
        soup = BeautifulSoup(content, features='html.parser')
        content = ''
        scripts = soup.select('script')
        # logger.info(scripts)
        for script in scripts:
            dom_referer = script.find(string=re.compile("document.write\(strencode"))
            if dom_referer is None: continue
            dst = context.eval(query_doc_write(script))
            # print(dst)
            # print('*' * 25)
            script.replace_with(dst)
        # print(str(soup).replace('&gt;', '>').replace('&lt;', '<'))
        content = str(soup).replace('&gt;', '>').replace('&lt;', '<')
    if len(content) > 0:
        soup = BeautifulSoup(content, features='html.parser')
        lists = soup.select('.row .col-lg-3')
        for item in lists:
            # print(item.prettify())
            dom_a = item.select_one('a')
            logging.info(f'dom_a: {dom_a}')
            if dom_a is None: continue
            url = dom_a['href']
            if len(url) <= 0: continue
            if 'viewkey=' not in url <= 0: continue
            key = re.search('viewkey=(([a-z0-9]*))', url).group(1)
            key = key.split('&', 1)[0]
            result_obj[key] = {'key': key, 'url': url, 'content_type': 'video'}
            dom_img = dom_a.select_one('img')
            logging.info(f'dom_img: {dom_img}')
            if dom_img:
                result_obj[key]['poster'] = dom_img['src']
            name_dom = dom_a.select_one('span.video-title')
            logging.info(f'name_dom: {name_dom}')
            if name_dom and name_dom.strings:
                result_obj[key]['name'] = str.strip(name_dom.string)
            logging.info(f'{key}: {result_obj[key]}')
    return result_obj

def load_accunt_list(uid, beg, end, show=True):
    # baseurl = 'http://91porn.com/uvideos.php?UID=' + uid + '&type=public&page=%s'
    baseurl = get_config('baseurl', 'http://www.91porn.com')
    baseurl = baseurl + '/uvideos.php?UID=' + uid + '&type=public&page=%s'
    return load_list(baseurl, uid, beg, end, show=show)


def load_rf_list(beg, end, show=True):
    # http://91porn.com/video.php?category=rf&page=1
    # rfbaseurl = 'http://91porn.com/video.php?category=rf&page=%s'
    baseurl = get_config('baseurl', 'http://www.91porn.com')
    rfbaseurl = baseurl + '/v.php?category=rf&page=%s'
    return load_list(rfbaseurl, 'rf', beg, end, show=show)


def delete_files(src, poster):
    src_local = f'{base_dir}/{src}'
    if os.path.exists(src_local):
        logging.info(f'[-]delete: {src_local}')
        os.remove(src_local)
    else:
        logging.info(f'[skip]delete: {src_local}')
    poster_local = f'{base_dir}/{poster}'
    if os.path.exists(poster_local):
        logging.info(f'[-]delete: {poster_local}')
        os.remove(poster_local)
    else:
        logging.info(f'[skip]delete: {poster_local}')

def check_keys(keys, show=True):
    result_obj = {}
    for index, key in enumerate(keys, start=1):
        try:
            item = loaddatadb(key, "Porn91")
            # 下载文件
            logging.info(f'[-] task[{key}] {index}/{len(keys)}')
            if not item or not item.src:
                logging.warning(f'[-] item[{key}]: {item}')
                dumpdatadb({key: {'status': -1}}, "Porn91")
                continue
            src = item.src
            data = {'status': -1}
            filename = resource_name(src)
            src_local = f'{videodir}/{filename.rsplit(".", 1)[0]}.mp4'
            if not os.path.exists(src_local):
                logging.warning(f'[-] src_local not exists: {src_local}')
                dumpdatadb({key: {'status': -1}}, "Porn91")
                continue
            poster = item.poster
            postername = resource_name(poster)
            poster_local = f'{posterdir}/{postername}'
            if not os.path.exists(poster_local):
                logging.warning(f'[-] poster_local not exists: {poster_local}')
        except KeyboardInterrupt as e:
            logging.info(f'[-] Stop: {e}')
            return
        except BaseException as e:
            logging.error(f'[{key}]ERROR: {e}')
            if "Event loop stopped" in str(e):
                dumpdatadb({key: {'status': -1}}, "Porn91")
                break



def handle_params(argv, show=True):
    logging.info(f'argv: {argv}')
    start_t = time.time()
    if '-p' in argv:
        arg_l = arg_list('-p', argv)
        if len(arg_l) <= 0:
            raise BaseException(f"[-]-p [addr:port]: {arg_l}")
        if ':' not in arg_l[0]:
            raise BaseException(f"[-]-p [addr:port]: {arg_l[0]}")
        addr, port = arg_l[0].split(':')
    if '-k' in argv:
        arg_l = arg_list('-k', argv)
        if len(arg_l) <= 0:
            raise BaseException(f"[-]-k key: {arg_l}")
        key = arg_l[0]
        # save_file(key, resource_name(key))
        # return
        get_url(key)
        data = get_parse_source(key)
        print(data)
        datas = {}
        datas[key] = data
        dumpdatadb(datas, "Porn91")
        print(data)
        print('[-]spend: %ds' % int(time.time() - start_t))
        return
    if '--download' in argv:
        arg_l = arg_list('--download', argv)
        if len(arg_l) <= 0:
            raise BaseException("[-]--download key: %s" % arg_l)
        key = arg_l[0]
        item = loaddatadb(key, "Porn91")
        data = {}
        if item and item.name and item.src:
            data = {'name': item.name, 'src': item.src}
        else:
            get_url(key)
            data = get_parse_source(key)
            datas = {}
            datas[key] = data
            dumpdatadb(datas, "Porn91")
        print(data)
        print('[-]get src spend: %ds' % int(time.time() - start_t))
        filename = '%s.mp4' % data['name']
        start_t = time.time()
        desc = {}
        save_file(data['src'], '%s/%s' % (videodir, filename), desc=desc)
        print(f'desc: {desc}')
        print('[-]download video spend: %ds' % int(time.time() - start_t))
        return
    if '-u' in argv:
        arg_l = arg_list('-u', argv)
        if len(arg_l) <= 0:
            raise BaseException("[-]-u url [filename]: %s" % arg_l)
        url = arg_l[0]
        filename = resource_name(url)
        if len(arg_l) >= 2:
            filename = arg_l[1]
        if '/' in filename:
            os.makedirs(filename.rsplit('/', 1)[0], exist_ok=True)
        # download(url, filename)
        return
    if '--load_accunt_list' in argv:
        # 下载列表
        # uid = 'ef08MeQxYBviUu16X3K8oIWSIsHvlJ4DikvVmnEhaZFAFlGD'
        # (beg,end] = 1:9
        arg_l = arg_list('--load_accunt_list', argv)
        if len(arg_l) <= 0:
            raise BaseException(
                "[-]--load_accunt_list uid [range]: %s" % arg_l)
        uid = arg_l[0]
        range_ = "1:2"
        if len(arg_l) >= 2 and ':' in arg_l[1]:
            match_ = re.match("^(\d+)\:(\d+)$", arg_l[1])
            if match_ and int(match_.group(1)) >= 1 and int(match_.group(1)) < int(match_.group(2)):
                range_ = arg_l[1]
        beg, end = range_.split(":")
        result = load_accunt_list(uid, int(beg), int(end), show)
        dumpdatadb(result, "Porn91")
        return
    if '--load_rf_list' in argv:
        arg_l = arg_list('--load_rf_list', argv)
        range_ = "1:2"
        if len(arg_l) > 0:
            match_ = re.match("^(\d+)\:(\d+)$", arg_l[0])
            if match_ and int(match_.group(1)) >= 1 and int(match_.group(1)) < int(match_.group(2)):
                range_ = arg_l[0]
        beg, end = range_.split(":")
        result = load_rf_list(int(beg), int(end), show)
        dumpdatadb(result, "Porn91")
        return
    if '--parse_list' in argv:
        arg_l = arg_list('--parse_list', argv)
        if len(arg_l) <= 0: return
        file_path = arg_l[0]
        result = parse_list(file_path)
        logging.info(result)
        return
    if '--import_keys' in argv:
        arg_l = arg_list('--import_keys', argv)
        keys = [item.key for item in load_items("Porn91", keys=arg_l)]
        import_keys(keys, show)
        return
    if '--update_keys' in argv:
        arg_l = arg_list('--update_keys', argv)
        keys = [item.key for item in load_items("Porn91", keys=arg_l)]
        update_keys(keys)
        return
    if '--download_keys' in argv:
        arg_l = arg_list('--download_keys', argv)
        keys = [item.key for item in load_items("Porn91", keys=arg_l)]
        download_keys(keys, show)
        return
    if '--check_keys' in argv:
        arg_l = arg_list('--check_keys', argv)
        keys = [item.key for item in load_items("Porn91", keys=arg_l)]
        check_keys(keys, show)
        return
    if '--get_parse_source' in argv:
        arg_l = arg_list('--get_parse_source', argv)
        if len(arg_l) < 1:
            raise BaseException("[-]--get_parse_source <key>: %s" % arg_l)
        key = arg_l[0]
        print(get_parse_source(key))
        return
    if '--stop_keys' in argv:
        arg_l = arg_list('--stop_keys', argv)
        if len(arg_l) <= 0:
            raise BaseException('--stop_keys key1, key2')
        files = [resource_name(item.src) for item in load_items("Porn91", keys=arg_l, filter={'status': 0})]
        for filename in files:
            if threading.Lock().acquire(True):
                result = None
                filename = f'{videodir}/{filename}.msg.json'
                dumpdatadb({filename: {'key': filename, 'content': json.dumps({'_status': False}, ensure_ascii=False)}}, 'Downinfo')
                # if not os.path.exists(filename):
                #     continue
                # with open(filename, 'r') as src:
                #     result = json.load(src)
                #     result['_status'] = False
                # if not result:
                #     continue
                # with open(filename, 'w') as src:
                #     json.dump(result, src)
        return
    if '--delete_keys' in argv:
        arg_l = arg_list('--delete_keys', argv)
        if len(arg_l) <= 0:
            raise BaseException('--delete_keys src poster')
        delete_files(arg_l[0], arg_l[1])
        return
    if '--proxytest' in argv:
        filename = '%s/proxy.status' % base_dir
        if os.path.exists(filename):
            with open(filename, 'r') as src:
                result = json.load(src)
            with open(filename, 'w') as src:
                # 'start': time.time(), '_start': datetime.now().strftime('%Y%m%d %H:%M:%S.%f')
                now = time.time()
                result['start'] = now
                result['_start'] = time.strftime(
                    '%Y%m%d %H:%M:%S', time.localtime(now))
                json.dump(result, src)
            logging.info('[beg]%s' % result)
            cip = '%s/cip.cc' % pagedir
            if os.path.exists(cip):
                os.remove(cip)
            desc = {}
            save_file('http://cip.cc', cip, desc=desc, blocks=1)
            print('status: %s' % desc.get('status', False))
            if desc.get('status', False) and os.path.exists(cip):
                with open(cip, 'r') as src:
                    result['data'] = src.read()
                    result['end'] = time.time()
            else:
                result['data'] = 'Failed to proxy'
                result['end'] = result['start'] - 1
            result['run'] = False
            with open(filename, 'w') as src:
                json.dump(result, src)
            logging.info('[end]%s' % result)
        else:
            logging.warning('[-]file %s not exists' % filename)
        return
    if '--thumbnails' in argv:
        arg_l = arg_list('--thumbnails', argv)
        if len(arg_l) <= 0:
            raise BaseException('--thumbnails keys')
        keys = [item.key for item in load_items("Porn91", keys=arg_l)]
        thumbnails_keys(keys)
        return
    if '-t':
        print('test')

        return
    if '--start_server':
        print('test')

        return

    print(help_msg)


class ClientDaemon(CDaemon):
    def __init__(self, name, save_path, stdin=os.devnull, stdout=os.devnull, stderr=os.devnull, home_dir='.', umask=0x022, verbose=1):
        super(ClientDaemon, self).__init__(save_path, stdin, stdout, stderr, home_dir, umask, verbose)
        self._name = name

    def run(self, argv):
        handle_params(argv, False)


def daemon(argv):
    arg_l = arg_list('-d', argv)
    if len(arg_l) <= 0 or arg_l[0] not in ['start', 'stop', 'restart', 'status', 'alive']:
        raise BaseException('[-] -d <start|stop|restart|status|alive>: %s' % arg_l)
    p_name = '91porn'
    p_dir = '%s/daemon' % base_dir
    os.makedirs(p_dir, exist_ok=True)
    cD = ClientDaemon(p_name, '%s/%s.pid' % (p_dir, p_name), stderr='%s/%s.error' %
                      (p_dir, p_name), stdout='%s/%s.log' % (p_dir, p_name), verbose=1)
    if arg_l[0] == 'start':
        cD.start(argv)
    elif arg_l[0] == 'stop':
        cD.stop()
    elif arg_l[0] == 'restart':
        cD.restart(argv)
    elif arg_l[0] == 'alive':
        return cD.is_running()
    elif arg_l[0] == 'status':
        alive = cD.is_running()
        if alive:
            print('process [%s] is running ......' % cD.get_pid())
        else:
            print('daemon process [%s] stopped' % cD._name)


help_msg = '''\
    Usage:python3 %s [-p <addr:port>]
    -d <start|stop|restart|status>              |daemon
    -k <key>                                    |根据key更新视频信息
    -u <url> [filename]                         |下载文件
    -p <addr:port>                              |代理
    --download <key>                            |根据key更新视频信息并下载
    --load_accunt_list <uid> [range]            |根据uid获取视频信息
    --load_rf_list [range]                      |获取热门视频信息
    --import_keys [key...]                      |下载视频页
    --update_keys [key...]                      |更新视频信息
    --download_keys [key...]                    |下载视频
    --get_parse_source <key>                    |解析播放页
    ---------------------------------------
    dependence
    ---------------------------------------
    aiohttp==3.6.2
    async-timeout==3.0.1
    attrs==19.3.0
    beautifulsoup4==4.9.1
    brotlipy==0.7.0
    certifi==2020.6.20
    cffi==1.14.0
    chardet==3.0.4
    idna==2.10
    idna-ssl==1.1.0
    Js2Py==0.70
    multidict==4.7.6
    pycparser==2.20
    pycryptodome==3.9.8
    pyjsparser==2.7.1
    PySocks==1.7.1
    pytz==2020.1
    PyYAML==5.3.1
    requests==2.24.0
    six==1.15.0
    soupsieve==2.0.1
    SQLAlchemy==1.3.18
    typing-extensions==3.7.4.2
    tzlocal==2.1
    urllib3==1.25.9
    yarl==1.4.2
    ---------------------------------------
''' % sys.argv[0]
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(help_msg)
    else:
        set_logger()
        if '-d' in sys.argv:
            daemon(sys.argv)
            exit(0)
        else:
            handle_params(sys.argv)
