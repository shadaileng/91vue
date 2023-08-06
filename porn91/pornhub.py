#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, sys, json, re, time, logging, threading
import js2py
# import execjs

from datetime import datetime
from bs4 import BeautifulSoup

from main import loaddatadb, dumpdatadb
from utils.download import open_sock5
from utils.download import resource_name
from utils.logger import set_logger
from utils.daemon import CDaemon

from config.settings import config
from main import get_config, load_items
from download import download_file_range, download_file_mulity, download_m3u8
from download.utils import resource_fullname

baseurl = 'https://cn.pornhub.com/view_video.php?viewkey=%s'
base_dir = config['base_dir']
pagedir = '%s/pages' % base_dir
posterdir = '%s/poster' % base_dir
m3u8dir = '%s/m3u8' % base_dir
jsdir = '%s/js' % base_dir

os.makedirs(pagedir, exist_ok = True)
os.makedirs(posterdir, exist_ok = True)
os.makedirs(m3u8dir, exist_ok = True)
os.makedirs(jsdir, exist_ok = True)

def save_file(url, filename, desc={}, *, verbose=False, blocks=512, headers={}, **kwargs):
    # headers=dict({'Cookie': get_config('pornhubcookie')}, **headers)
    proxy = get_config('proxy', 'socks5://127.0.0.1:1080')
    download_file_range(url, filename, desc=desc, blocks=blocks, verbose=verbose, proxy=proxy, headers=headers, **kwargs)

def save_m3u8(url, filename, desc={}, *, verbose=False, blocks=512):
    headers={}
    proxy = get_config('proxy', 'socks5://127.0.0.1:1080')
    download_m3u8(url, filename, desc=desc, blocks=blocks, verbose=verbose, proxy=proxy, headers=headers)

def download_multifile(tasks=[], *, verbose=False, **kw):
    headers={'Cookie': get_config('91cookie')}
    proxy = get_config('proxy', 'socks5://127.0.0.1:1080')
    download_file_mulity(tasks, verbose=verbose, proxy=proxy, headers=headers)

def get_parse_source(key):
    content = ''
    with open('%s/%s.html' % (pagedir, key), 'r') as dst:
        content = dst.read()
    data = {}
    soup = BeautifulSoup(content, features='html.parser')

    name = soup.find('meta', {'name': 'twitter:title'})['content'].strip()
    data['name'] = name

    url = soup.find('meta', {'property': 'og:url'})['content'].strip()
    data['url'] = url
    key = re.search('viewkey=(.+)', url).group(1)
    data['key'] = key
    poster = soup.find('meta', {'property': 'og:image'})['content'].strip()
    data['poster'] = poster

    dom_info = soup.find('script', {'type': 'application/ld+json'}, string=re.compile('"uploadDate"'))
    if dom_info:
        info = json.loads(dom_info.string)
        duration = info.get('duration', None)
        if duration:
            repx = re.search('PT(\d+)H(\d+)M(\d+)S', duration)
            if repx and repx.group(1):
                data['duration']= int(repx.group(1)) * 60 * 60 + int(repx.group(2)) * 60 + int(repx.group(3))
        uploadDate = info.get('uploadDate', None)
        if uploadDate:
            publish_date = datetime.strptime(uploadDate, '%Y-%m-%dT%H:%M:%S+00:00')
            data['publish_stamp']= publish_date.timestamp()
            data['publish_date']= publish_date.strftime('%Y%m%d')
        data['uname']=info.get('author', None)
    '''
    dom_src_code = soup.select('#player > script')[0]
    # code = '%sreturn qualityItems_329988412;' % dom_src_code.string
    code = '%sfunction getSrc(){return qualityItems_329988412;};' % dom_src_code.string
    filename_ = 'dist/js/desktop-player-adaptive.min.js'
    if not os.path.exists(filename_):
        save_file('https://cdn1d-static-shared.phncdn.com/html5player/videoPlayer/html5/4.1.7/desktop-player-adaptive.min.js', filename_, is_text=True, blocks=1)
    env_code = ''
    src = None
    with open(filename_, 'r') as dst:
        env_code = dst.read()
    src = execjs.eval(env_code)
    # src = execjs.eval(code)
    src = execjs.eval('%s;%s' % (env_code, code))
    # with PyV8.JSContext() as ctx:
    #     src = ctx.eval('%s;%s' % (env_code, code))
    # context = js2py.EvalJs()
    # context.execute(env_code)
    # src = cogenerate_cookientext.eval(code)
    print(src)
    '''
    print(data)
    return data

def generate_cookie(url, filename):
    content = ''
    with open(filename, 'r') as dst:
        content = dst.read()
    data = {}
    soup = BeautifulSoup(content, features='html.parser')
    if len(str(soup.find('body'))) > 100: return '' 
    dom_code = soup.select('script')
    src = ''
    if dom_code:
        code = dom_code.string.replace('document.cookie=', 'return ')
        context = js2py.EvalJs()
        src = context.eval(code)
    return src
    
def get_url(key):
    save_file(baseurl % key, '%s/%s.html' % (pagedir, key))
    cookie = generate_cookie(baseurl % key, '%s/%s.html' % (pagedir, key))
    if len(cookie) > 0:
        save_file(baseurl % key, '%s/%s.html' % (pagedir, key), headers={"Cookie": cookie})
    return get_parse_source(key)


def import_keys(keys, show=True):
    '''
    异步下载,避免429错误,并发次数3
    '''
    base_url = 'https://cn.pornhub.com/view_video.php?viewkey=%s'
    # baseurl % key, '%s/%s.html' % (pagedir, key)
    
    # 下载播放页面
    result={}
    try:
        result_obj = {}
        for key in keys:
            result_obj[key] = {'key': key, 'status': 0}
        dumpdatadb(result_obj, "PornHub")
        tasks = [get_url(key) for key in keys]
        # tasks = [(base_url % key, '%s/%s.html' % (pagedir, key))for key in keys]
        # download_multifile(tasks, verbose=show)
    except KeyboardInterrupt as e:
        logging.warning('[-]exit')
        logging.info('[-] Stop: %s' % e)
    # except BaseException as e:
    #     logging.error('[-]Error: %s' % str(e))
    #     logging.info('[-] Stop: %s' % e)
    result_obj = {}
    for key in keys:
        result_obj[key] = {'key': key, 'status': -1}
    dumpdatadb(result_obj, "PornHub")

def update_keys(keys):
    '''
    批量解析播放页面
    '''
    for key in keys:
        try:
            item = loaddatadb(key, "PornHub")
            if item:
                dumpdatadb({key: {'status': 0}}, "PornHub")
            data = get_url(key)
            data['status'] = -1
            dumpdatadb({key: data}, "PornHub")
            logging.info('[-] Success update[%s]' % key)
        except KeyboardInterrupt as e:
            logging.info('[-] Stop: %s' % e)
            dumpdatadb({key: {'status': -1}}, "PornHub")
            return
        except BaseException as e:
            logging.error('[%s]ERROR: %s' % (key, e))
            dumpdatadb({key: {'status': -2}}, "PornHub")

def download_keys(keys, show=True):
    result_obj = {}
    for index, key in enumerate(keys, start=1):
        try:
            item = loaddatadb(key, "PornHub")
            # 下载文件
            logging.info('[-] task[%s] %s/%s' % (key, index, len(keys)))
            if not item.src or item.status == 1: 
                logging.warning('[skip] src of item[%s] is %s' % (key, item.src))
                continue
            dumpdatadb({key: {'status': 0}}, "PornHub")
            # 下载视频
            src = item.src
            filename = resource_fullname(src)
            src_local = '%s/%s' % (m3u8dir, filename)
            desc = {}
            save_m3u8(src, src_local, desc=desc, verbose=show)
            data_src = {'src_local': 'm3u8/%s' % filename, 'duration': desc.get('duration', 0)}
            dumpdatadb({key: data_src}, "PornHub")
            # 下载封面
            poster = item.poster
            postername = resource_name(poster)
            poster_local = '%s/%s' % (posterdir, postername)
            if not os.path.exists(poster_local):
                save_file(poster, poster_local, verbose=show, blocks=4)
                data_poster = {'poster_local': 'poster/%s' % postername}
                dumpdatadb({key: data_poster}, "PornHub")
            dumpdatadb({key: {'status': 1}}, "PornHub")
        except KeyboardInterrupt as e:
            logging.info('[-] Stop: %s' % e)
            dumpdatadb({key: {'status': -1}}, "PornHub")
            return
        except BaseException as e:
            logging.error('[%s]ERROR: %s' % (key, e))
            if "Event loop stopped" in str(e):
                dumpdatadb({key: {'status': -1}}, "PornHub")
                break
            dumpdatadb({key: {'status': -2}}, "PornHub")

def load_list(base_url, flag, beg, end, show=True):
    '''
    异步下载,避免429错误,并发次数3
    '''
    keys = [index for index in range(beg, end)]
    rand = datetime.now().strftime('%Y%m%d')
    files = ['%s/%s-%s-%s.html' % (pagedir, flag, key, rand) for key in keys]
    tasks = [(base_url % key, '%s/%s-%s-%s.html' % (pagedir, flag, key, rand)) for key in keys]
    download_multifile(tasks, verbose=show)
    result_obj = {}
    for filename in files:
        content = ''
        with open(filename, 'r', encoding="utf-8",errors='ignore') as dst:
            content = dst.read()
        soup = BeautifulSoup(content, features='html.parser')
        lists = soup.select('#wrapper .row .col-sm-12 .row .col-xs-12.col-sm-4.col-md-3.col-lg-3')
        for item in lists:
            dom_a = item.select_one('a')
            url = dom_a['href']
            key = re.search('viewkey=(([a-z0-9]*))&', url).group(1)
            result_obj[key] = {'key': key, 'url': url, 'content_type': 'video'}
            dom_span = item.select_one('.video-title')
            if dom_span:
                result_obj[key]['name'] = dom_span.string
            dom_img = item.select_one('img')
            if dom_img:
                result_obj[key]['poster'] = dom_img['src']
    return result_obj

def load_accunt_list(uid, beg, end, show=True):
    baseurl = 'http://91porn.com/uvideos.php?UID=' + uid + '&type=public&page=%s'
    return load_list(baseurl, uid, beg, end, show=show)

def load_rf_list(beg, end, show=True):
    # http://91porn.com/video.php?category=rf&page=1
    rfbaseurl = 'http://91porn.com/video.php?category=rf&page=%s'
    return load_list(rfbaseurl, 'rf', beg, end, show=show)

def arg_list(flag, argv):
    argv_l = []
    for index in range(argv.index(flag) + 1, len(argv)):
        if argv[index].startswith('-'): break
        argv_l.append(argv[index])
    return argv_l

def handle_params(argv, show=True):
    logging.info('argv: %s' % argv)
    start_t = time.time()
    if '-k' in argv:
        arg_l = arg_list('-k', argv)
        if len(arg_l) <= 0: raise BaseException("[-]-k key: %s" % arg_l)
        key = arg_l[0]
        #save_file(key, resource_name(key))
        #return
        data = get_url(key)
        print(data)
        datas = {}
        datas[key] = data
        dumpdatadb(datas, "PornHub")
        print(data)
        print('[-]spend: %ds' % int(time.time() - start_t))
        return
    if '--load_accunt_list' in argv:
        # 下载列表
        # uid = 'ef08MeQxYBviUu16X3K8oIWSIsHvlJ4DikvVmnEhaZFAFlGD'
        # (beg,end] = 1:9
        arg_l = arg_list('--load_accunt_list', argv)
        if len(arg_l) <= 0: raise BaseException("[-]--load_accunt_list uid [range]: %s" % arg_l)
        uid = arg_l[0]
        range_ = "1:2"
        if len(arg_l) >= 2 and ':' in arg_l[1]:
            range_ = arg_l[1]
        beg, end = range_.split(":")
        result = load_accunt_list(uid, int(beg), int(end), show)
        dumpdatadb(result, "PornHub")
        return
    if '--load_rf_list' in argv:
        arg_l = arg_list('--load_rf_list', argv)
        range_ = "1:2"
        if len(arg_l) > 0 and ':' in arg_l[0]:
            range_ = arg_l[0]
        beg, end = range_.split(":")
        result = load_rf_list(int(beg), int(end), show)
        dumpdatadb(result, "PornHub")
        return
    if '--import_keys' in argv:
        arg_l = arg_list('--import_keys', argv)
        import_keys(arg_l, show)
        return
    if '--update_keys' in argv:
        arg_l = arg_list('--update_keys', argv)
        update_keys(arg_l)
        return
    if '--download_keys' in argv:
        arg_l = arg_list('--download_keys', argv)
        keys = [item.key for item in load_items("PornHub", keys=arg_l)]
        download_keys(keys, show)
        return
    if '--get_parse_source' in argv:
        arg_l = arg_list('--get_parse_source', argv)
        if len(arg_l) < 1: raise BaseException("[-]--get_parse_source <key>: %s" % arg_l)
        key = arg_l[0]
        print(get_parse_source(key))
        return
    if '--stop_keys' in argv:
        arg_l = arg_list('--stop_keys', argv)
        if len(arg_l) <= 0: raise BaseException('--stop_keys key1, key2')
        files = [resource_name(item.src) for item in load_items("PornHub", keys=arg_l, filter={'status': 0})]
        for filename in files:
            if threading.Lock().acquire(True):
                result = None
                filename = '%s/%s.msg.json' % (m3u8dir, filename)
                if not os.path.exists(filename): continue
                with open(filename, 'r') as src:
                    result = json.load(src)
                    result['_status'] = False
                if not result: continue
                with open(filename, 'w') as src:
                    json.dump(result, src)
        return
    if '-t':
        print('test')
    print(help_msg)

class ClientDaemon(CDaemon):
    def __init__(self, name, save_path, stdin=os.devnull, stdout=os.devnull, stderr=os.devnull, home_dir='.', umask=0x022, verbose=1):
        super(ClientDaemon, self).__init__(save_path, stdin, stdout, stderr, home_dir, umask, verbose)
        self._name = name
    def run(self, argv):
        handle_params(argv, False)

def daemon(argv):
    arg_l = arg_list('-d', argv)
    if len(arg_l) <= 0 or arg_l[0] not in ['start', 'stop', 'restart', 'status', 'alive']: raise BaseException('[-] -d <start|stop|restart|status|alive>: %s' % arg_l)
    p_name = '91porn'
    p_dir = '%s/daemon' % base_dir
    os.makedirs(p_dir, exist_ok = True)
    cD = ClientDaemon(p_name, '%s/%s.pid' % (p_dir, p_name), stderr='%s/%s.error' % (p_dir, p_name), stdout='%s/%s.log' % (p_dir, p_name), verbose=1)
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
            print('daemon process [%s] stopped' %cD._name)

help_msg = '''\
    Usage:python3 %s [-p <addr:port>]
    -d <start|stop|restart|status>              |daemon
    -k <key>                                    |根据key更新视频信息
    -p <addr:port>                              |代理
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
    # open_sock5('127.0.0.1', 1080)
    # key = '8fee3a14588603f34535'
    if len(sys.argv) < 2:
        print(help_msg)
    else:
        set_logger()
        if '-d' in sys.argv:
            daemon(sys.argv)
            exit(0)
        else:
            handle_params(sys.argv)
