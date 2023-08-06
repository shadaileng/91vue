#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging, asyncio, json, os
from aiohttp import web
from aioweb import corelib, settings
from utils import import_code
from utils import background_task
from main import get_config
from download import Download


routes = web.RouteTableDef()
module_name = 'haijiao'

@routes.get(f'/{module_name}/topic')
async def parse_topic(request):
    try:
        params = await corelib.parse_param(request)
        topid = params.get('topid', None)
        if topid is None:
            return {'code': -1, 'field': 'topid', 'msg': 'topid is empty'}
        user = request.__user__ if hasattr(request, '__user__') else None
        user_id = 0
        if user:
            user_id = user['id']
        haijiao = await corelib.load_item('Attachment', filter={'key': 'haijiao'})
        if haijiao:
            haijiao = haijiao.get('content')
            haijiao = import_code(haijiao, 'haijiao')
            task = await background_task.add_task(haijiao.main, [topid])
            print(task)
        # background_task.add_task
        data = {'code': 0, 'msg': f'开始解析{topid}'}
        return data
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
        return {'code': -1, 'msg': str(e)}

@routes.get(f'/{module_name}/uid')
async def parse_uid(request):
    try:
        params = await corelib.parse_param(request)
        uid = params.get('uid', None)
        if uid is None:
            return {'code': -1, 'field': 'uid', 'msg': 'uid is empty'}
        user = request.__user__ if hasattr(request, '__user__') else None
        user_id = 0
        if user:
            user_id = user['id']
        haijiao = await corelib.load_item('Attachment', filter={'key': 'haijiao'})
        if haijiao:
            haijiao = haijiao.get('content')
            haijiao = import_code(haijiao, 'haijiao')
            task = await background_task.add_task(haijiao.main_list, uid)
            print(task)
        # background_task.add_task
        data = {'code': 0, 'msg': f'开始解析{uid}'}
        return data
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
        return {'code': -1, 'msg': str(e)}

@routes.post(f'/{module_name}/download')
async def download(request):
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
        haijiao = await corelib.load_item('Attachment', filter={'key': 'haijiao'})
        if haijiao:
            haijiao = haijiao.get('content')
            haijiao = import_code(haijiao, 'haijiao')
            task = await background_task.add_task(download, items, haijiao)
            logging.info(f'[+] task start: {task}')
        # background_task.add_task
        data = {'code': 0, 'msg': f'开始下载任务...'}
        return data
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
        return {'code': -1, 'msg': str(e)}


async def download(items, haijiao):
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
                task = await haijiao.main_img(item['poster'])
                poster_local = f"poster/{os.path.basename(item['poster']).rsplit('.', 1)[0]}"
                if not os.path.exists(f'{settings.config["base_dir"]}/{poster_local}'):
                    logging.warning(f'[-] task[{key}] poster_local not exists: {poster_local}')
                else:
                    item['poster_local'] = poster_local
            else:
                logging.warning(f"[skip] task[{key}] poster is null: {item}")
        except BaseException as e:
            logging.error(f'[{key}]ERROR: {e}')
            if "Event loop stopped" in str(e):
                item['status'] = -1
                break
            item['status'] = -2
        logging.info(f'[-] dump {key}: {item}')
        corelib.save('Porn91', [item])


@routes.post(f'/{module_name}/poster')
async def update_poster(request):
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
        haijiao = await corelib.load_item('Attachment', filter={'key': 'haijiao'})
        if haijiao:
            haijiao = haijiao.get('content')
            haijiao = import_code(haijiao, 'haijiao')
            task = await background_task.add_task(poster, items, haijiao)
            logging.info(f'[+] task start: {task}')
        # background_task.add_task
        data = {'code': 0, 'msg': f'开始更新封面...'}
        return data
    except BaseException as e:
        logging.error(corelib.printException(e))
        return {'code': -1, 'msg': str(e)}


async def poster(items, haijiao):
    for index, item in enumerate(items, start=1):
        try:
            key = item.get("key", None)
            if key is None:
                logging.warning(f'[skip] key is null: {item}')
                continue
            logging.info(f'[-] task[{key}] {index}/{len(items)}')
            topid = os.path.basename(item.get('url', ''))
            if len(topid) <= 0: 
                logging.warning(f'[skip] topid is null: {item}')
                continue
            item_ = await haijiao.main([topid])
            
            if len(item_) > 0 and item_[0].get('poster', None) is not None: 
                task = await haijiao.main_img(item_[0]['poster'])
                poster_local = f"poster/{os.path.basename(item_[0]['poster']).rsplit('.', 1)[0]}"
                if not os.path.exists(f'{settings.config["base_dir"]}/{poster_local}'):
                    logging.warning(f'[-] task[{key}] poster_local not exists: {poster_local}')
                else:
                    item['poster_local'] = poster_local
            else:
                logging.warning(f"[skip] task[{key}] poster is null: {item_}")
        except BaseException as e:
            logging.error('\n%s' % corelib.printException(e))
            if "Event loop stopped" in str(e):
                break
