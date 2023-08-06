#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging, os, io
import time, asyncio, json
from aiohttp import web, WSMsgType
from aioweb import corelib
from utils.server import send_task

import main

routes = web.RouteTableDef()
module_name = 'porn91'

@routes.get('/')
@corelib.template('index.html')
async def index(request):
    data = {}
    try:
        params = await corelib.parse_param(request)
        path = params.get('path', '/root')
    except BaseException as e:
        logging.error('[-]Error: %s' % e)
    return data


@routes.get('/vue/items')
async def get_items(request):
    data = {}
    try:
        user = request.__user__ if hasattr(request, '__user__') else None
        params = await corelib.parse_param(request)
        path = params.get('path', '/root')
        index = int(params.get('index', '1'))
        pagesize = int(params.get('pagesize', '36') if len(params.get('pagesize', '36')) > 0 else '36')
        path = params.get('path', '/root')
        #############
        status = params.get('status', None)
        name = params.get('name', None)
        uname = params.get('uname', None)
        filter = {'status': status, 'path': path}
        like = {'name': name, 'uname': uname}
        if user is None:
            pagesize = 0
        elif pagesize <= 0:
            pagesize = 15
        page = await corelib.load_page("Porn91", index, pagesize=pagesize, filter=filter, like=like, order_by={'publish_date': False, 'created_date': False})
        for item in page['items']:
            src_local = item['src_local']
            src_exists = src_local is not None and os.path.exists(os.path.join(main.setting('base_dir'), f'{src_local.rsplit(".", 1)[0]}.png'))
            thumbnails = f'{src_local.rsplit(".", 1)[0]}.png' if src_exists else False
            item['thumbnails'] = thumbnails
        data['path'] = path[1:].split('/')
        if status != None:
            data['status'] = status
        if uname != None:
            data['uname'] = uname
        data = dict(data, **page)
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
        data = {'items': [], 'path': ['root']}
    data['prefix'] = '/'
    return web.json_response({'code': 0, 'data': data})

@routes.get('/item/{id}')
async def item(request):
    data = {}
    try:
        id = request.match_info['id']
        item = await corelib.load_item("Porn91", filter={'id': id})
        data['items'] = [item] if item else []
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
    return web.json_response({'code': 0, 'data': data})


@routes.post('/import')
async def import_91(request):
    try:
        params = await corelib.parse_param(request)
        items = params.get('items', [])
        if len(items) <= 0:
            return {'code': -1, 'field': 'items', 'msg': 'items is empty'}
        user = request.__user__ if hasattr(request, '__user__') else None
        user_id = 0
        if user:
            user_id = user['id']
        keys = [item.get('key', '') for item in items]
        items_exists = await corelib.load_items('Porn91', in_={'key': keys})
        for item_ in items:
            for item in items_exists['items']:
                if item_['key'] == item['key']:
                    item_['id'] = item['id']
                    break
        corelib.save('Porn91', items)
        data = {'code': 0, 'msg': '导入成功'}
        return data
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
        return {'code': -1, 'msg': str(e)}


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
        # keys = [item.get('key', '') for item in items]
        # items_exists = await corelib.load_items('Porn91', in_={'key': keys})
        # items_exists = items_exists['items']
        # user = request.__user__ if hasattr(request, '__user__') else None
        # user_id = 0
        # if not user:
        #     return {'code': -1, 'field': 'user', 'msg': '请登录'}
        keys = [item['key'] for item in items]
        argv = ['-d', '--delete_keys'] + keys
        send_task(argv)
        corelib.delete('Porn91', [item.get('id', None) for item in items])
        data = {'code': 0, 'msg': '删除成功'}
        return data
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
        return {'code': -1, 'msg': str(e)}


@routes.get('/configs')
async def configs(request):
    data = {}
    try:
        params = await corelib.parse_param(request)
        items = await corelib.load_items("Config")
        data = dict(data, **items)
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
    return web.json_response({'code': 0, 'data': data})

@routes.post('/configs')
async def do_configs(request):
    data = {}
    try:
        params = await corelib.parse_param(request)
        items = params.get('items', [])
        if len(items) <= 0:
            return {'code': -1, 'field': 'items', 'msg': 'items is empty'}
        corelib.save('Config', items)
        items = await corelib.load_items("Config")
        data = dict(data, **items)
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
    return {'code': 0, 'msg': data}


@routes.post('/configs/del')
async def del_configs(request):
    data = {}
    try:
        params = await corelib.parse_param(request)
        ids = params.get('ids', [])
        if len(ids) <= 0:
            return {'code': -1, 'field': 'ids', 'msg': 'ids is empty'}
        corelib.delete('Config', ids)
        items = await corelib.load_items("Config")
        data = dict(data, **items)
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
    return {'code': 0, 'msg': data}


@routes.post('/update_poster')
async def update_poster(request):
    try:
        params = await corelib.parse_param(request)
        keys = params['keys']
        data_obj = {}
        cdn = main.get_config('cdn')
        if not cdn:
            return web.json_response({'code': -1, 'msg': "未设置cdn"})
        st = main.get_config('st')
        if not st:
            return web.json_response({'code': -1, 'msg': "未设置st"})
        for key in keys:
            item = main.loaddatadb(key, "Porn91")
            if not item:
                continue
            if not item.poster or len(item.poster) <= 0:
                logging.warning("[%s]: %s" % (key, item))
                continue
            num = item.poster.rsplit("/", 1)[1].split(".", 1)[0]
            item_ = {
                'src': '%s//%s/%s.m3u8?st=%s&e=%s' % (cdn, num, num, st, int(time.time()))}
            logging.info("设置src: %s" % item_)
            data_obj[key] = item_
            # 发送指令下载封面暂时不开通
        main.dumpdatadb(data_obj, "Porn91")
        return web.json_response({'code': 0, 'msg': 'save ok'})
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
        return web.json_response({'code': -1, 'msg': str(e)})


@routes.post('/download')
async def download(request):
    try:
        params = await corelib.parse_param(request)
        keys = params['keys']
        # items = params['items']
        # keys = [item['key'] for item in items]
        items = await corelib.load_items("Porn91", in_={"key": keys})
        filename = f'back_{int(time.time())}.tar.gz'
        file_path = os.path.join(main.setting('base_dir'), filename)
        # files = await main.make_tarfile(items['items'])
        files = await main.make_tarfile_name(items['items'], file_path)
        return {'code': 0, 'msg': f'[download] {files} -> {filename}'}
        #     with open(file_path, 'rb') as f:
        #         content = f.read()
        #     if content:
        #         response = web.Response(
        #             content_type='application/octet-stream',
        #             headers={'Content-Disposition': f'attachment;filename={filename}'},
        #             body=content)
        # # response = web.Response(
        # #         content_type='application/octet-stream',
        # #         headers={'Content-Disposition': f'attachment;filename={filename}'},
        # #         body=files['data'].getvalue())
        # return response
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
        return {'code': -1, 'msg': '[download] %s' % str(e)}

'''
后台任务
'''

@routes.post('/loadrflist')
async def load_rf_list(request):
    try:
        params = await corelib.parse_param(request)
        range_ = params.get('range', '')
        argv = ['--load_rf_list'] + [range_]
        send_task(argv)
        return {'code': 0, 'msg': '[loadrflist] success'}
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
        return {'code': -1, 'msg': '[loadrflist] %s' % str(e)}


@routes.post('/loadaccuntlist')
async def load_accunt_list(request):
    try:
        params = await corelib.parse_param(request)
        range_ = params.get('range', '')
        uname = params.get('uname', '')
        if len(uname) <= 0:
            return {'code': -1, 'msg': '[loadaccuntlist] uname[%s] is null ' % uname}
        argv = ['--load_accunt_list', uname] + [range_]
        send_task(argv)
        return {'code': 0, 'msg': '[loadaccuntlist] success'}
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
        return {'code': -1, 'msg': '[loadaccuntlist] %s' % str(e)}


@routes.post('/loadvideopage')
async def loadvideopage(request):
    try:
        params = await corelib.parse_param(request)
        items = params['items']
        keys = [item['key'] for item in items]
        argv = ['-d', '--update_keys'] + keys
        send_task(argv)
        return {'code': 0, 'msg': '[loadvideopage] begin'}
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
        return {'code': -1, 'msg': str(e)}


@routes.post('/downloadsrc')
async def downloadsrc(request):
    try:
        params = await corelib.parse_param(request)
        items = params['items']
        keys = [item['key'] for item in items]
        argv = ['-d', '--download_keys'] + keys
        send_task(argv)
        return {'code': 0, 'msg': '[downloadsrc] begin'}
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
        return {'code': -1, 'msg': str(e)}


@routes.post('/check_keys')
async def check_keys(request):
    try:
        params = await corelib.parse_param(request)
        items = params['items']
        keys = [item['key'] for item in items]
        argv = ['-d', '--check_keys'] + keys
        send_task(argv)
        return {'code': 0, 'msg': '[check_keys] begin'}
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
        return {'code': -1, 'msg': str(e)}


@routes.post('/stop')
async def stop(request):
    try:
        params = await corelib.parse_param(request)
        items = params['items']
        keys = [item['key'] for item in items]
        argv = ['--stop_keys'] + keys
        send_task(argv)
        return {'code': 0, 'msg': '[stop] success'}
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
        return {'code': -1, 'msg': str(e)}

@routes.get('/rebootDService')
async def rebootDService(request):
    try:
        return {'code': 0, 'msg': '[rebootDService] success'}
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
        return {'code': -1, 'msg': str(e)}

@routes.post('/thumbnails')
async def thumbnails(request):
    try:
        params = await corelib.parse_param(request)
        items = params['items']
        keys = [item['key'] for item in items]
        argv = ['-d', '--thumbnails'] + keys
        send_task(argv)
        return web.json_response({'code': 0, 'msg': '正在更新视频预览'})
    except BaseException as e:
        return web.json_response({'code': -1, 'msg': str(e)})

@routes.get('/tail')
async def logger_handle(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    filename = f"{main.setting('base_dir')}/logs/server/info.log"
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
                        filename = f"{main.setting('base_dir')}/logs/{msg.data.strip().split(' ', 1)[1]}"
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



@routes.get('/tail1')
async def websocke_handle1(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    filename = '%s/logs/server/info.log' % main.setting('base_dir')
    with open(filename, 'rb') as src:
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                if msg.data == 'close':
                    logging.warning('[-]close')
                    await ws.close()
                elif msg.data.startswith('1'):
                    lines = src.readlines()
                    for line in lines[-10:]:
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
            elif msg.type == WSMsgType.ERROR:
                logging.error('ws connection closed with exception %s' % ws.exception())
    logging.warning('websocket connection closed')

    return ws


@routes.get('/status')
async def websocke_handle(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    local_dict = {'filename': ''}
    async for msg in ws:
        if msg.type == WSMsgType.TEXT:
            await asyncio.sleep(1)
            text = msg.data
            # print(text)
            data = {'command': '', 'params': {}}
            try:
                data = json.loads(text)
            except json.decoder.JSONDecodeError as e:
                data['command'] = text
            if data['command'] == 'close':
                logging.warning('[-]close')
                await ws.close()
            elif data['command'].startswith('key'):
                for key in data['params']:
                    item = await main.status_key(key, 'Porn91')
                    if item is None: continue
                    rep = {'command': 'rep', 'params': item}
                    await ws.send_str(json.dumps(rep))
            elif data['command'].startswith('path'):
                key = data['params']['key']
                path = data['params']['path']
                item = await main.status_path(key, path)
                rep = {'command': 'rep', 'params': item}
                await ws.send_str(json.dumps(rep))
            elif data['command'].startswith('running'):
                # running.status
                item = await main.status_path('running', 'video/running.status')
                filename = item.get('filename', None)
                if filename is not None and local_dict.get('filename', None) != filename:
                    key_num = os.path.splitext(os.path.basename(filename))[0]
                    item_ = await corelib.load_item("Porn91", like={'src': key_num})
                    if item_:
                        local_dict['item'] = item_
                    local_dict['filename'] = filename
                item['item'] = local_dict.get('item', None)
                rep = {'command': 'running', 'params': item}
                await ws.send_str(json.dumps(rep))
            else:
                logging.info(msg.data + '/answer')
                await ws.send_str(msg.data + '/answer')
        elif msg.type == WSMsgType.ERROR:
            logging.error(f'ws connection closed with exception {ws.exception()}')
    # await asyncio.sleep(5)
    # logging.info('req ...')
    # await ws.send_str('req')
    logging.warning('websocket connection closed')

    return ws


@routes.get('/ws')
async def websocke_handle2(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    async for msg in ws:
        print(msg)
        if msg.type == WSMsgType.TEXT:
            if msg.data == 'close':
                logging.warning('[-]close')
                await ws.close()
            elif msg.data.startswith('1status'):
                key = msg.data.split(' ', 1)[1]
                await main.downloading(key, ws)
            else:
                await ws.send_str(msg.data + '/answer')
        elif msg.type == WSMsgType.ERROR:
            logging.error('ws connection closed with exception %s' %
                        ws.exception())
    logging.warning('websocket connection closed')

    return ws


