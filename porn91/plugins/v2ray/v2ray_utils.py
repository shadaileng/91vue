#!/usr/bin/python3
# -*- coding: utf-8 -*-

from asyncio.log import logger
import os, re
import json
from site import abs_paths
import subprocess
import time
import asyncio
import logging

from sqlalchemy import true
from . import main

from urllib.request import unquote
from ping3 import ping
import psutil


cwdAbsPath = os.path.abspath(os.path.dirname(__file__))


def create_vmess(url, sub):
    protocol, base64_str = url.split('://', 1)
    server = json.loads(main.base64_decode(base64_str.encode('utf8')))
    # server['ps'] = ps = server['ps'].encode('utf8').decode('unicode_escape')
    server['url'] = url
    server['sub'] = sub
    server['protocol'] = protocol

    # output(server)
    return server


def create_ss(url, sub):
    protocol, base64_str = url.split('://', 1)
    ps, addr, port = ('', '', '')
    if '#' in base64_str:
        base64_str, ps = base64_str.split('#', 1)
        ps = unquote(ps, encoding='utf-8')
    # base64_str += (4 - len(base64_str) % 4) * '='
    if '@' in base64_str:
        base64_str, ip_port = base64_str.split('@', 1)
        base64_str += (4 - len(base64_str) % 4) * '='
        decode_str = main.base64_decode(base64_str.encode('utf8'))
        addr, port = ip_port.split(':')
        base64_str += (4 - len(base64_str) % 4) * '='
        crypt, pw = decode_str.split(":")
    else:
        base64_str += (4 - len(base64_str) % 4) * '='
        decode_str = main.base64_decode(base64_str.encode('utf8'))
        if '@' in decode_str:
            decode_str, ip_port = decode_str.split('@', 1)
            crypt, pw = decode_str.split(":")
            addr, port = ip_port.split(':')
    re_port = re.search(r'(\d+)', port)
    if re_port and re_port.group(1):
        port = re_port.group(1)
    server = {
        "ps": ps,
        "add": addr,
        "port": int(port),
        "scy": crypt,
        "password": pw,
        'url': url,
        'sub': sub,
        'protocol': protocol,
    }
    # output(server)
    return server


def output(server):
    print('-' * 65)
    print('%s: %s' % (server['sub'], server['url']))
    print(json.dumps(server, indent=4))


def update_subs(urlstr, sub=''):
    urls = urlstr.split('\n')
    servers = []
    for item in urls:
        if '://' in item:
            if item.startswith('vmess://'):
                servers.append(create_vmess(item, sub))
            elif item.startswith('ss://'):
                servers.append(create_ss(item, sub))
    keyRelate = [('url', 'url'), ('protocol', 'protocol'),
                 ('subscribe', 'sub'), ('address', 'add'),
                 ('port', 'port'), ('password', 'password'),
                 ('key', 'id'), ('aid', 'aid'),
                 ('security', 'scy'), ('remarks', 'ps'),
                 ('network', 'net'), ('type', 'type'),
                 ('host', 'host'), ('tls', 'tls'), ('path', 'path')]
    v2rays = [{key1: server.get(key2, '') for (
        key1, key2) in keyRelate} for server in servers]
    # print(v2rays)
    return v2rays
    # save_v2ray(servers)


def update_subs_file(filename, sub=''):
    urlstr = main.base64_decode_file(filename)
    return update_subs(urlstr, sub)


def update_subs_text(text, sub=''):
    urlstr = main.base64_decode(text.encode('utf8'))
    result = update_subs(urlstr, sub)
    return result


def parse_config(v2ray):
    outbound = {}
    if v2ray['protocol'] == 'vmess':
        outbound = {
            "tag": "proxy",
            "protocol": "vmess",
            "settings": {
                "vnext": [
                    {
                        "address": v2ray['address'],
                        "port": int(v2ray['port']),
                        "users": [
                            {
                                "id": v2ray['key'],
                                "alterId": int(v2ray['aid']),
                            }
                        ],
                    }
                ]
            },
            "streamSettings": {
                "network": v2ray['network'],
                "security": v2ray['tls'] if v2ray['tls'] else "none",
                # "sockopt": {
                #     "mark": 255
                # },
                "tlsSettings": {
                    "allowInsecure": False,
                    "serverName": v2ray['host']
                },
                "wsSettings": {
                    "path": v2ray['path'],
                    "headers": {
                        "Host": v2ray['host']
                    }
                },
                "mux": {
                    "enabled": False,
                    "concurrency": -1
                }
            },
        }
    elif v2ray['protocol'] == 'ss':
        outbound = {
            "tag": "proxy",
            "protocol": "shadowsocks",
            "settings": {
                "servers": [
                    {
                        "address": v2ray['address'],
                        "port": v2ray['port'],
                        "method": v2ray['security'],
                        "password": v2ray['password'],
                    }
                ]
            },
            "streamSettings": {
                "sockopt": {
                    "mark": 255
                }
            }
        }
    return outbound

def init_inbounds(argv={}):
    return [
    {
      "tag": "socks",
      "port": argv.get('socks_port', 1080),
      "listen": argv.get('listen', "127.0.0.1"),
      "protocol": "socks",
      "sniffing": {
        "enabled": True,
        "destOverride": [
          "http",
          "tls"
        ]
      },
      "settings": {
        "auth": "noauth",
        "udp": True,
        "allowTransparent": False
      }
    },
    {
      "tag": "http",
      "port": argv.get('http_port', 1081),
      "listen": argv.get('listen', "127.0.0.1"),
      "protocol": "http",
      "sniffing": {
        "enabled": True,
        "destOverride": [
          "http",
          "tls"
        ]
      },
      "settings": {
        "udp": False,
        "allowTransparent": False
      }
    }
  ]

def render_config(tName, out_argv, in_argv={'listen': "127.0.0.1", 'socks_port': 1080, 'http_port': 1081}):
    tpath = os.path.join(os.path.join(cwdAbsPath, 'templates'), tName)
    with open(tpath) as src:
        TEST_CONFIG = json.load(src)
    outbound = parse_config(out_argv)
    TEST_CONFIG["inbounds"] = init_inbounds(in_argv)
    TEST_CONFIG["outbounds"].insert(0, outbound)
    return json.dumps(TEST_CONFIG, indent=4)


def _create_v2ray_subporcess(exe, config_name: str) -> subprocess.Popen:
    logging.info("启动v2ray进程...")
    process = subprocess.Popen(
        [exe, "-config", config_name],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        cwd=os.path.join(cwdAbsPath, 'v2ray')
    )
    time.sleep(1.3)
    return process


def create_v2ray_subporcess(exe, config_name):
    process = _create_v2ray_subporcess(exe, config_name)
    if not check_process(process):
        logging.info("重建v2ray进程...")
        return _create_v2ray_subporcess(exe, config_name)
    return process


def check_process(process: subprocess.Popen) -> bool:
    if process.poll():
        logging.warning("v2ray执行失败,尝试杀死所有v2ray进程")
        for proc in psutil.process_iter(["name", "username"]):
            if proc.name() == "v2ray_test":
                proc.kill()
        return False
    return True


def _get_download_speed_():
    event_loop = asyncio.get_event_loop()
    return_value = None
    cum = []
    tasks = [main.download('https://www.google.com', timeout=10,
                           proxy="socks5://127.0.0.1:10086") for i in range(0, 3)]
    return_value = event_loop.run_until_complete(asyncio.wait(tasks))
    result = [item.result()[1] for item in iter(return_value[0])]
    cum = [item['duration'] for item in result if item['duration'] > 0]
    return round(sum(cum) / len(cum) * 1000, 3) if len(cum) > 0 else -1


async def get_download_speed(config, port=1080) -> float:
    speed = 0.0
    logging.info(f"开始测试 {config['remarks']} 服务...")
    speed = round(await _get_download_speed(port), 3)
    if speed >= 1800000 or speed < 0:
        logging.info(f"测试 {config['remarks']} 服务超时...")
        speed = -1.0
    return speed


async def _get_download_speed(port=1080):
    return_value = None
    cum = []
    # tasks = [main.download('https://www.cip.cc', timeout=10) for i in range(0, 3)]
    # tasks = [main.download('https://www.google.com', timeout=10, proxy="socks5://127.0.0.1:10086") for i in range(0, 3)]
    num = 3
    url = 'https://www.google.com'
    tasks = [main.download(
        url, timeout=20, proxy=f"socks5://127.0.0.1:{port}") for i in range(0, num)]
    result = await asyncio.gather(*tasks)
    cum = [item[1]['duration'] for item in result if item[1]['duration'] > 0]
    return round(sum(cum) / len(cum) * 1000, 3) if len(cum) > 0 else -1


async def check_v2ray():
    for proc in psutil.process_iter(["name", "username"]):
        if 'v2ray_enable' in proc.name():
            port = [conn.laddr.port for conn in psutil.net_connections() if conn.pid ==
                    proc.pid]
            return True, proc, port
    return (False,)


async def kill_v2ray(port=1080):
    config_name = os.path.abspath(os.path.join(cwdAbsPath, f"v2ray/{port}_config.json"))
    pid_file = os.path.abspath(os.path.join(cwdAbsPath, f"v2ray/{port}.pid"))
    result = await run_command(f'sh ./v2ray.sh stop v2ray_enable 1 {pid_file}', os.path.join(cwdAbsPath, 'v2ray'))
    logger.info(f"stop: {result}")
    if os.path.exists(config_name):
        os.remove(config_name)
    if os.path.exists(pid_file):
        os.remove(pid_file)
    # for proc in psutil.process_iter(["name", "username"]):
    #     if 'v2ray_enable' in proc.name():
    #         logging.info(f'关闭v2ray进程: {proc}')
    #         proc.terminate()
    #         return True, proc
    # return False


async def enable_v2ray(server, port=1080):
    '''
    启动V2ray
    '''
    config_name = os.path.abspath(os.path.join(cwdAbsPath, f"v2ray/{port}_config.json"))
    with open(config_name, 'w') as fp:
        in_argv={'listen': "127.0.0.1", 'socks_port': port, 'http_port': port+1}
        fp.write(render_config('v2ray_enable.json.j2', server, in_argv))
    # process = create_v2ray_subporcess('./v2ray_enable', config_name)
    # return check_process(process)
    pid_file = os.path.abspath(os.path.join(cwdAbsPath, f"v2ray/{port}.pid"))
    result = await run_command(f'sh ./v2ray.sh reload v2ray_enable {config_name} {pid_file}', os.path.join(cwdAbsPath, 'v2ray'))
    logger.info(f"reload: {result}")
    await asyncio.sleep(5)
    return True


       
async def run_command(cmd, cwd=None):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=cwd)
    stdout, stderr = await proc.communicate()
    result = f'[{cmd!r} exited with {proc.returncode}]\n'
    if stdout:
        result += f'[stdout]\n{stdout.decode()}'
    if stderr:
        result += f'[stderr]\n{stderr.decode()}'
    return result


async def test_v2ray(server, port=1080):
    ping_s = ping(server['address'])
    if ping_s is None:
        return 'ping[%s]: -1' % server['address'], False
    logging.info('ping[%s]: %sms' %
                 (server['address'], round(ping_s * 1000, 3)))
    config_name = os.path.abspath(os.path.join(
        cwdAbsPath, f"v2ray/{port}_config.json"))
    pid_file = os.path.abspath(os.path.join(cwdAbsPath, f"v2ray/{port}.pid"))
    with open(config_name, 'w') as fp:
        in_argv={'listen': "127.0.0.1", 'socks_port': port, 'http_port': port+1}
        fp.write(render_config('v2ray_test.json.j2', server, in_argv))
    speed = -1
    result = await run_command(f'sh ./v2ray.sh reload v2ray_test {config_name} {pid_file}', os.path.join(cwdAbsPath, 'v2ray'))
    logger.info(f"reload: {result}")
    await asyncio.sleep(5)
    for index in range(3):
        logging.info(f"测试第{index + 1}次...")
        #'''
        speed = await get_download_speed(server, port)
        print(f'[{speed}]')
        if speed > 0:
            break
        #'''
        '''
        process = create_v2ray_subporcess('./v2ray_test', config_name)
        if not check_process(process):
            logging.info(f"第{index + 1}次失败,重试...")
            time.sleep(1.5)
            continue
        else:
            speed = await get_download_speed(server)
            process.terminate()
            if speed > 0:
                break
        '''
    # logging.info(f'切换工作目录{cwd}')
    # os.chdir(cwd)
    result = await run_command(f'sh ./v2ray.sh stop v2ray_test 1 {pid_file}', os.path.join(cwdAbsPath, 'v2ray'))
    logger.info(f"stop: {result}")
    if os.path.exists(config_name):
        os.remove(config_name)
    if os.path.exists(pid_file):
        os.remove(pid_file)
    
    return '%sms' % speed, speed > 0

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--parse", help="parse <filename|text|url>",
                        action="store_true", dest="is_parse", default=False)
    parser.add_argument("-t", "--test", help="test <filename|text|url>",
                        action="store_true", dest="is_test", default=False)
    parser.add_argument("--async", help="async ",
                        action="store_true", dest="is_async", default=False)
    parser.add_argument("-d", "--download", help="download <url>",
                        action="store_true", dest="is_download", default=False)
    parser.add_argument("-c", "--check_v2ray", help="check_v2ray <url>",
                        action="store_true", dest="is_check_v2ray", default=False)
    parser.add_argument("--text", help="--text <text>")
    parser.add_argument("--filename", help="--filename <filename>")
    parser.add_argument("--url", help="--url <vemss|ss>")
    args = parser.parse_args()
    logging.info(args)
    # print(args)

    if args.is_async:
        event_loop = asyncio.get_event_loop()
        if args.is_test:
            v2rays = []
            if args.filename is not None:
                v2rays = update_subs_file(args.filename)
            elif args.text is not None:
                v2rays = update_subs_text(args.text)
            elif args.url is not None:
                v2rays = update_subs(args.url)
            else:
                parser.print_help()
                exit(0)
            return_value = event_loop.run_until_complete(
                asyncio.wait([test_v2ray(v2ray) for v2ray in v2rays]))
            result = [item.result() for item in iter(return_value[0])]
            print(result)
        if args.is_check_v2ray:
            return_value = event_loop.run_until_complete(
                asyncio.wait([check_v2ray()]))
            result = [item.result() for item in iter(return_value[0])]
            print(result)
        exit(0)
    if args.is_parse:
        if args.filename is not None:
            v2rays = update_subs_file(args.filename)
        if args.text is not None:
            v2rays = update_subs_text(args.text)
        if args.url is not None:
            v2rays = update_subs(args.url)
        print(v2rays)
    if args.is_download:
        # if args.url:
        # _get_download_speed()
        pass
