# -*- coding: utf-8 -*-

import asyncio
import time
import os
import json, random

import aiohttp

import re, subprocess


# 将日志输出的时间类型转换成秒
def get_seconds(time):
    h = int(time[0:2])
    # print("时：" + str(h))
    m = int(time[3:5])
    # print("分：" + str(m))
    s = int(time[6:8])
    # print("秒：" + str(s))
    ms = int(time[9:12])
    # print("毫秒：" + str(ms))
    ts = (h * 60 * 60) + (m * 60) + s + (ms / 1000)
    return ts

def test_process():
    # size= 25189kB time=00:04:28.67 bitrate= 768.0kbits/s speed= 748x
    # video:0kB audio:25189kB subtitle:0kB other streams:0kB global headers:0kB muxing overhead: 0.000302%
    src = 'https://la3.killcovid2021.com/m3u8/806253/806253.m3u8'
    name = 'dist/video/806253.mp4'
    command = f'ffmpeg -y -allowed_extensions ALL -protocol_whitelist "file,http,https,crypto,tcp"  -i {src} -c  copy  {name}'
    command = f'ffmpeg -threads 16  -y -allowed_extensions ALL -protocol_whitelist "file,http,https,tls,crypto,tcp" -i {src} -c  copy -bsf:a aac_adtstoasc {name}'
    # command = 'ffmpeg -y -allowed_extensions ALL -protocol_whitelist "file,http,crypto,tcp" -i %s.m3u8 -c copy %s' % (_name, name)
    print(command)
    # process = subprocess.Popen(command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8", text=True)
    processrun = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8", text=True)
    with open('dist/logs/status_806253.log', 'w') as log_dst:
        for line in processrun.stdout:
            # print(line)
            log_dst.write(line)
            log_dst.flush()
            duration_res = re.search(r'\sDuration: (?P<duration>\S+)', line)
            if duration_res is not None:
                duration = duration_res.groupdict()['duration']
                duration = re.sub(r',', '', duration)
                result = re.search(r'\stime=(?P<time>\S+)', line)
                if result is not None:
                    elapsed_time = result.groupdict()['time']
                    # 此处可能会出现进度超过100%，未对数值进行纠正
                    progress = (get_seconds(elapsed_time) / get_seconds(duration)) * 100
                    print(elapsed_time)
                    print(progress)
                    print("进度:%3.2f" % progress + "%")
                    # processrun.wait()
                    if processrun.poll() == 0:
                        print("success:", processrun)
                    # else:
                    #     print("error:", processrun)

def test_text():
    line = 'frame= 1696 fps= 22 q=-1.0 size=    1280kB time=00:00:33.88 bitrate= 309.5kbits/s speed=0.435x'
    result = re.search(r'\stime=(?P<time>\S+)', line)
    print(result)
    elapsed_time = result.groupdict()['time']
    print(elapsed_time)
    print(get_seconds(elapsed_time))


# test_process()

async def stdout(msg):
    print(msg)


async def timeout(flag):
    print(flag)
    await asyncio.sleep(5)
    flag['run'] = False
    print(flag)

def logger():
    path = 'dist/server/info.log'
    with open(path, 'a') as src:
        index = 0
        while index < 100:
            text = f'{time.time()}\n'
            print(text)
            src.write(text)
            src.flush()
            time.sleep(1)
            index += 1

def status():
    path = 'dist/video/639362.m3u8.status1'
    sta = {"total": 115117996, "scale": 0.0, "speed": 0.00, "threadNum": 100}
    with open(path, 'w') as src:
        index = 0
        while index < 100:
            index += int(random.random() * 15)
            if index > 100: index = 100
            sta['scale'] = index
            sta['speed'] = random.random() * 5 + 1002250
            sta['threadNum'] = 100 - index
            text = json.dumps(sta)
            print(text)
            src.seek(0)
            src.truncate()
            src.write(text)
            src.flush()
            time.sleep(1)

def dump_status():
    with open('dist/tmp.txt', 'w') as src:
        src.seek(0)
        src.truncate()
        src.write("12")
        src.flush()

def test_head():
    async def main():
        async with aiohttp.ClientSession() as session:
            async with session.get('http://httpbin.org/get') as resp:
                rsp = {'status': resp.status}
                rsp['headers'] = {key: resp.headers[key] for key in resp.headers}
                print(rsp)
                text = await resp.text()
                print(len(text))
                print(text)

    asyncio.run(main())

import types

def import_code(code, name):
    # create blank module
    module = types.ModuleType(name)
    # populate the module with code
    exec(code, module.__dict__)
    return module

code = r'''
def log(text):
    print(text)
'''

from utils import lmdb_utils
lmdb_path = f"/data/lmdb"
env = lmdb_utils.init(lmdb_path)

lmdb_utils.display(env)

if __name__ == '__main__':
    pass
    # test = import_code(code, 'test')
    # test.log('hello')
    # from porn91 import save_file
    # save_file('https://cdn77.91p49.com/m3u8/742639/742639.m3u8', '/data/video/742639.m3u8')
    # test_head()

    # from porn91 import parse_list
    # print(parse_list('./dist/pages/rf-1-20220717.html'))
    '''
    from porn91 import decode_doc_write
    src = 'strencode2("%20%3c%73%70%61%6e%20%63%6c%61%73%73%3d%64%33%64%39%34%34%36%38%30%32%61%34%34%32%35%39%37%35%35%64%33%38%65%36%64%31%36%33%65%38%32%30%3e")'
    src = decode_doc_write(src)
    print(src)
    '''
    '''
    from porn91 import parse_list
    # data = parse_list('dist/pages/rf-1-20220719.html')
    data = parse_list('dist/pages/2481c9d81fb77fd79262.html')
    print(data)
    '''
