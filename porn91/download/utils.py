# -*- coding: utf-8 -*-

import sys, os, json, random, logging, re, main
import requests
from urllib import request
from urllib.error import URLError
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

def resource_fullname(url):
    url = url.split('?', 1)[0] if '?' in url else url
    return url.rsplit('://', 1)[1] if '://' in url else url

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
    except KeyboardInterrupt as e:
        raise e
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
        return main.loaddata(filename)
    except KeyboardInterrupt as e:
        raise e
    except BaseException as e:
        logging.warning('[-]Error[%s]: %s' % (sys.exc_info()[2].tb_lineno, e))
    return None

def dumpdata(filename, data):
    try:
        return main.dumpdata(filename, data)
    except KeyboardInterrupt as e:
        raise e
    except BaseException as e:
        logging.error('[-]Error[%s]: %s' % (sys.exc_info()[2].tb_lineno, e))
        if isinstance(e, KeyboardInterrupt): raise e
    return False


def get_resource_size(url, *, headers={}):
    '''
    获取资源大小
    :params: url-请求的url地址
    :return: total-资源大小,mt-是否支持多线程
    '''
    total = 0
    mt = False
    headers = dict(add_header(), **headers)
    headers['Range'] = 'bytes=0-4'
    logging.info('[-]wget %s' % url)
    proxies = {'http': 'socks5://127.0.0.1:1080', 'https': 'socks5://127.0.0.1:1080'}
    resp = requests.head(url, headers=headers, proxies=proxies, verify=False)
    # resp.status_code, resp.reason
    headers = resp.headers
    print(headers)
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
    return (total, mt)
