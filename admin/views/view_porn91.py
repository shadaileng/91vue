#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging, asyncio, os, time
from aiohttp import web, WSMsgType
from aioweb import corelib, settings
from utils import import_code, background_task
from main import get_config, loaddatadb, dumpdatadb, make_tarfile_name
from download import Download, thumbnails

routes = web.RouteTableDef()
module_name = 'porn91'

@routes.post(f'/{module_name}/loadvideopage')
async def loadvideopage(request):
    try:
        params = await corelib.parse_param(request)
        items = params['items']
        keys = [item['key'] for item in items]
        porn91 = await corelib.load_item('Attachment', filter={'key': '91porn'})
        if not porn91:
            return {'code': -1, 'msg': f'脚本[91porn]不存在'}
        porn91 = porn91.get('content')
        porn91 = import_code(porn91, 'porn91')
        task_name = f'loadvideopage'
        if task_name in background_task.background_tasks.keys():
            return {'code': -1, 'msg': f'任务[{task_name}]运行中...'}
        task = await background_task.add_task(task_name, porn91.main, keys)
        logging.info(f'[+] task start: {task}')
        return {'code': 0, 'msg': f'开始解析[{task_name}]...'}
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
        return {'code': -1, 'msg': str(e)}

@routes.post(f'/{module_name}/loadrflist')
async def parse_rflist(request):
    try:
        params = await corelib.parse_param(request)
        page_range = params.get('page_range', '1:2')
        if page_range is None:
            return {'code': -1, 'field': 'page_range', 'msg': 'page_range is empty'}
        user = request.__user__ if hasattr(request, '__user__') else None
        user_id = 0
        if user:
            user_id = user['id']
        porn91 = await corelib.load_item('Attachment', filter={'key': '91porn'})
        if not porn91:
            return {'code': -1, 'msg': f'脚本[91porn]不存在'}
        porn91 = porn91.get('content')
        porn91 = import_code(porn91, 'porn91')
        if page_range in background_task.background_tasks.keys():
            return {'code': -1, 'msg': f'任务[{page_range}]运行中...'}
        task = await background_task.add_task(page_range, porn91.load_rf_list, page_range)
        logging.info(f'[+] task start: {task}')
        return {'code': 0, 'msg': f'开始解析[{page_range}]...'}
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
        return {'code': -1, 'msg': str(e)}

@routes.post(f'/{module_name}/loadaccuntlist')
async def parse_acctlist(request):
    try:
        params = await corelib.parse_param(request)
        uname = params.get('uname', None)
        page_range = params.get('page_range', '1:2')
        if uname is None:
            return {'code': -1, 'field': 'uname', 'msg': 'uname is empty'}
        if page_range is None:
            return {'code': -1, 'field': 'page_range', 'msg': 'page_range is empty'}
        user = request.__user__ if hasattr(request, '__user__') else None
        user_id = 0
        if user:
            user_id = user['id']
        porn91 = await corelib.load_item('Attachment', filter={'key': '91porn'})
        if porn91:
            porn91 = porn91.get('content')
            porn91 = import_code(porn91, 'porn91')
            task_name = f'{uname}_{page_range}'
            if task_name in background_task.background_tasks.keys():
                return {'code': -1, 'msg': f'任务[{task_name}]运行中...'}
            task = await background_task.add_task(task_name, porn91.load_acct_list, uname, page_range)
            logging.info(f'[+] task start: {task}')
        return {'code': 0, 'msg': f'开始解析{task_name}'}
    except BaseException as e:
        logging.error('%s' % corelib.printException(e))
        return {'code': -1, 'msg': str(e)}

async def task_calback(key, coroutine, *args, **kw):
    try:
        task = await background_task.add_task(key, coroutine, *args, **kw)
    except asyncio.CancelledError as e:
        logging.info(f'[{key}] cancel')
    except BaseException as e:
        logging.error(f'[{key}]ERROR: {e}')


@routes.post(f'/{module_name}/download')
async def doDownload(request):
    try:
        params = await corelib.parse_param(request)
        items = params.get('items', [])
        keys = [item.get('key', '') for item in items]
        items = await corelib.load_items('Porn91', in_={'key': keys})
        items = items.get('items', [])
        if len(items) <= 0:
            return {'code': -1, 'field': 'items', 'msg': 'items is empty'}
        user = request.__user__ if hasattr(request, '__user__') else None
        user_id = 0
        if user:
            user_id = user['id']
        task_name = f'download'
        if task_name in background_task.background_tasks.keys():
            return {'code': -1, 'msg': f'任务[{task_name}]运行中...'}
        task = await background_task.add_task(task_name, download, items)
        logging.info(f'[+] task start: {task}')
        return {'code': 0, 'msg': f'开始下载任务[{task_name}]...'}
    except BaseException as e:
        logging.error(corelib.printException(e))
        return {'code': -1, 'msg': str(e)}

async def download(items):
    for index, item in enumerate(items, start=1):
        try:
            key = item.get("key", None)
            if key is None:
                logging.warning(f'[skip] key is null: {item}')
                continue
            logging.info(f'[-] task[{key}] {index}/{len(items)}')
            if item.get('status', -1) == 1:
                logging.warning(f'[skip] task[{key}] status is 1: {item}')
                continue
            if item.get('src', None) is None:
                logging.warning(f"[skip] task[{key}] src is null: {item}")
                continue
            data = {key: {"key": key, "status": 0}}
            logging.info(f'[-] dump {key}: {data}')
            dumpdatadb(data, "Porn91")
            headers = {}
            desc = {}
            proxy = get_config('proxy')
            kw = {'desc': desc, 'blocks': 512, 'verbose': False, 'proxy': proxy, 'headers': headers}
            src_local = f'{settings.config["base_dir"]}/video/{os.path.basename(item["src"])}'
            await Download(**kw).download_m3u8(item['src'], src_local)
            src_local = f'video/{os.path.basename(item["src"]).rsplit(".", 1)[0]}.mp4'
            src_local_ = f"{settings.config['base_dir']}/{src_local}"
            if not os.path.exists(src_local_):
                logging.warning(f'[-] src_local not exists: {src_local_}')
                item['status'] = -2
            else:
                item['size'] = desc.get('size', 0)
                item['duration'] = desc.get('duration', 0)
                item['src_local'] = src_local
                item['status'] = 1
            if item.get('poster', None) is not None: 
                poster_local = f"poster/{os.path.basename(item['poster'])}"
                kw['blocks'] = 1
                kw['thread_num'] = 1
                await Download(**kw).download_file_range(item['poster'], f'{settings.config["base_dir"]}/{poster_local}')
                if not os.path.exists(f'{settings.config["base_dir"]}/{poster_local}'):
                    logging.warning(f'[-] task[{key}] poster_local not exists: {poster_local}')
                else:
                    item['poster_local'] = poster_local
            else:
                logging.warning(f"[skip] task[{key}] poster is null: {item}")
        except asyncio.CancelledError as e:
            logging.info(f'[{key}] cancel')
            item['status'] = -1
            logging.info(f'[-] dump {key}: {item}')
            corelib.save('Porn91', [item])
            break
        except BaseException as e:
            logging.error(f'[{key}]ERROR: {corelib.printException(e)}')
            if "Event loop stopped" in str(e):
                item['status'] = -1
                logging.info(f'[-] dump {key}: {item}')
                corelib.save('Porn91', [item])
                break
            item['status'] = -2
        logging.info(f'[-] dump {key}: {item}')
        corelib.save('Porn91', [item])


@routes.post('/thumbnails')
async def doThumbnails(request):
    try:
        params = await corelib.parse_param(request)
        items = params['items']
        keys = [item['key'] for item in items]
        task_name = f'thumbnails'
        if task_name in background_task.background_tasks.keys():
            return {'code': -1, 'msg': f'任务[{task_name}]运行中...'}
        task = await background_task.add_task(task_name, thumbnails_keys, keys)
        logging.info(f'[+] task start: {task}')
        return {'code': 0, 'msg': f'开始更新预览任务[{task_name}]...'}
    except BaseException as e:
        return {'code': -1, 'msg': str(e)}

async def thumbnails_keys(keys):
    result_obj = {}
    for index, key in enumerate(keys, start=1):
        try:
            logging.info(f'[-] task[{key}] {index}/{len(keys)}')
            item = loaddatadb(key, "Porn91")
            if not item.src_local:
                logging.info(f'src_local 为空: {item.src_local}')
                continue
            src = os.path.join(settings.config['base_dir'], item.src_local)
            # print(ffmpeg.probe(src)['streams'])
            duration = await thumbnails(src, f'{src.rsplit(".", 1)[0]}.png')
            dumpdatadb({item.key: {'duration': duration}}, "Porn91")
        except asyncio.CancelledError as e:
            logging.info(f'[{key}] cancel')
            break
        except BaseException as e:
            logging.error(f'[ERROR]{key}: {repr(e)}')

@routes.post('/check_keys')
async def doCheckKeys(request):
    try:
        params = await corelib.parse_param(request)
        items = params['items']
        keys = [item['key'] for item in items]
        task_name = f'check_keys'
        if task_name in background_task.background_tasks.keys():
            return {'code': -1, 'msg': f'任务[{task_name}]运行中...'}
        task = await background_task.add_task(task_name, check_keys, keys)
        logging.info(f'[+] task start: {task}')
        return {'code': 0, 'msg': f'开始检查任务[{task_name}]...'}
    except BaseException as e:
        return {'code': -1, 'msg': str(e)}

async def check_keys(keys):
    for index, key in enumerate(keys, start=1):
        try:
            logging.info(f'[-] task[{key}] {index}/{len(keys)}')
            item = loaddatadb(key, "Porn91")
            if not item.src_local:
                logging.info(f'src_local 为空: {item.src_local}')
                dumpdatadb({key: {'status': -1}}, "Porn91")
                continue
            src_local = os.path.join(settings.config['base_dir'], item.src_local)
            if not os.path.exists(src_local):
                logging.warning(f'[-] task[{key}] src_local not exists: {src_local}')
                dumpdatadb({key: {'status': -1}}, "Porn91")
                continue
            poster_local = os.path.join(settings.config['base_dir'], item.poster_local)
            if not os.path.exists(poster_local):
                logging.warning(f'[-] task[{key}] poster_local not exists: {poster_local}')
            logging.info(f'[-] task[{key}] 检查完成')
        except asyncio.CancelledError as e:
            logging.info(f'task[{key}] cancel')
            break
        except BaseException as e:
            logging.error(f'[ERROR]task[{key}]: {repr(e)}')


@routes.post('/delete')
async def delete_91(request):
    try:
        params = await corelib.parse_param(request)
        items = params.get('items', [])
        if len(items) <= 0:
            return {'code': -1, 'field': 'items', 'msg': 'items is empty'}
        user = request.__user__ if hasattr(request, '__user__') else None
        user_id = 0
        if user:
            user_id = user['id']
        keys = [item['key'] for item in items]
        task_name = f'delete_keys'
        if task_name in background_task.background_tasks.keys():
            return {'code': -1, 'msg': f'任务[{task_name}]运行中...'}
        task = await background_task.add_task(task_name, delete_keys, keys)
        logging.info(f'[+] task start: {task}')
        corelib.delete('Porn91', [item.get('id', None) for item in items])
        return {'code': 0, 'msg': '删除成功'}
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
        return {'code': -1, 'msg': str(e)}


async def delete_keys(keys):
    for index, key in enumerate(keys, start=1):
        try:
            logging.info(f'[-] task[{key}] {index}/{len(keys)}')
            item = loaddatadb(key, "Porn91")
            src_local = os.path.join(settings.config['base_dir'], item.src_local)
            if os.path.exists(src_local):
                logging.info(f'[-]delete: {src_local}')
                os.remove(src_local)
            else:
                logging.info(f'[skip] task[{key}] src_local not exists: {src_local}')
            poster_local = os.path.join(settings.config['base_dir'], item.poster_local)
            if os.path.exists(poster_local):
                logging.info(f'[-]delete: {poster_local}')
                os.remove(poster_local)
            else:
                logging.warning(f'[skip] task[{key}] poster_local not exists: {poster_local}')
            logging.info(f'[-] task[{key}] 删除完成')
        except asyncio.CancelledError as e:
            logging.info(f'task[{key}] cancel')
            break
        except BaseException as e:
            logging.error(f'[ERROR]task[{key}]: {repr(e)}')

@routes.post('/package')
async def package(request):
    try:
        params = await corelib.parse_param(request)
        keys = params['keys']
        items = await corelib.load_items("Porn91", in_={"key": keys})
        task_name = f'package_keys'
        if task_name in background_task.background_tasks.keys():
            return {'code': -1, 'msg': f'任务[{task_name}]运行中...'}
        filename = f'back_{int(time.time())}.tar.gz'
        file_path = os.path.join(settings.config['base_dir'], filename)
        task = await background_task.add_task(task_name, make_tarfile_name, items['items'], file_path)
        logging.info(f'[+] task start: {task}')
        return {'code': 0, 'msg': f'打包任务[{task_name}]开始...'}
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
        return {'code': -1, 'msg': '[download] %s' % str(e)}


@routes.get('/tail')
async def logger_handle(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    filename = f"{settings.config['base_dir']}/logs/admin/info.log"
    src = None
    async for msg in ws:
        if msg.type == WSMsgType.TEXT:
            try:
                if msg.data == 'close':
                    if src is not None and isinstance(src, io.BufferedReader): src.close()
                    logging.warning('[-]close')
                    await ws.close()
                elif msg.data.startswith('1'):
                    if ' ' in msg.data.strip():
                        filename = f"{settings.config['base_dir']}/logs/{msg.data.strip().split(' ', 1)[1]}"
                    if not os.path.exists(filename):
                        logging.warning(f'[-] {filename} not exists, close websocke')
                        await ws.close()
                    src = open(filename, 'rb')
                    lines = src.readlines()
                    for line in lines[-15:]:
                        line = line.decode('utf-8').strip().strip('\n')
                        await ws.send_str(line)
                    lines = None
                    src.seek(0, 2)
                elif msg.data.startswith('2'):
                    await asyncio.sleep(0.1)
                    line = src.readline().decode('utf-8').strip().strip('\n')
                    if len(line) > 0:
                        await ws.send_str(line)
                    else:
                        await ws.send_str('')
                else:
                    await ws.send_str(msg.data + '/answer')
            except BaseException as e:
                logging.info('[-] Exception: %s' % e)
                await ws.close()
        elif msg.type == WSMsgType.ERROR:
            if src is not None and isinstance(src, io.BufferedReader): src.close()
            logging.error('ws connection closed with exception %s' % ws.exception())
    logging.warning('websocket connection closed')

    return ws
