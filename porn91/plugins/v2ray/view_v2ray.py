#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import json, asyncio
from aiohttp import web, WSMsgType
from aioweb import corelib

from . import main, v2ray_utils


routes = web.RouteTableDef()
module_name = 'v2ray'


@routes.get('/%s' % module_name)
@corelib.template('v2ray.html')
async def v2ray_index(request):
    data = {}
    try:
        params = await corelib.parse_param(request)
        path = params.get('path', '/root')
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
    return data


@routes.get('/%s/subs' % module_name)
async def v2ray_subs(request):
    data = {}
    try:
        # params = await corelib.parse_param(request)
        items = await corelib.load_items('Subscribe')
        items['items'] = main.filter_fields_dict_list(
            items['items'], ['id', 'name', 'url', 'enable', 'proxy'])
        data = dict(data, **items)
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
        data['items'] = []
    return web.json_response({'code': 0, 'msg': data})


@routes.post('/%s/subs/save' % module_name)
async def v2ray_subs_save(request):
    data = {}
    try:
        params = await corelib.parse_param(request)
        items = params['items']
        corelib.save('Subscribe', items)
        items = await corelib.load_items('Subscribe')
        items['items'] = main.filter_fields_dict_list(
            items['items'], ['id', 'name', 'url', 'enable', 'proxy'])
        data = dict(data, **items)
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
        return web.json_response({'code': -1, 'msg': str(e)})
    return web.json_response({'code': 0, 'msg': data})


@routes.post('/%s/subs/delete' % module_name)
async def v2ray_subs_delete(request):
    data = {}
    try:
        params = await corelib.parse_param(request)
        ids = params['ids']
        corelib.delete('Subscribe', ids)
        items = await corelib.load_items('Subscribe')
        items['items'] = main.filter_fields_dict_list(
            items['items'], ['id', 'name', 'url', 'enable', 'proxy'])
        data = dict(data, **items)
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
        return web.json_response({'code': -1, 'msg': str(e)})
    return web.json_response({'code': 0, 'msg': data})


@routes.get('/%s/items' % module_name)
async def v2ray_items(request):
    data = {}
    try:
        check_v2ray = await v2ray_utils.check_v2ray()
        if not check_v2ray[0]:
            items = await corelib.load_items('V2ray', in_={'enabled': True})
            if len(items['items']) > 0:
                items = items['items']
                for item in items:
                    item['enabled'] = False
                corelib.save('V2ray', items)
            else:
                await v2ray_utils.kill_v2ray()
        # params = await corelib.parse_param(request)
        items = await corelib.load_items('V2ray')
        # items['items'] = main.filter_fields_dict_list(items['items'], ['id', 'name', 'url', 'enable'])
        data = dict(data, **items)
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
        data['items'] = []
    return web.json_response({'code': 0, 'msg': data})


@routes.post('/%s/subs/update' % module_name)
async def v2ray_subs_update(request):
    data = {}
    try:
        params = await corelib.parse_param(request)
        items = params.get('items', [])
        for item in items:
            if not item['enable']:
                continue
            # main.update_subs_text
            proxy = None
            if item.get('proxy', False):
                proxy = 'socks5://127.0.0.1:1080'
            content, results = await main.download(item['url'], proxy=proxy)
            print('*' * 25)
            print(f'result: {results}, content: {content}')
            print('*' * 25)
            if content is None or len(content) <= 0:
                continue
                # return web.json_response({'code': -1, 'msg': '订阅获取内容失败: %s' % item['url']})
            v2rays = v2ray_utils.update_subs_text(content, item['name'])
            corelib.save('V2ray', v2rays)
        items = await corelib.load_items('V2ray')
        # items['items'] = main.filter_fields_dict_list(items['items'], ['id', 'name', 'url', 'enable'])
        data = dict(data, **items)
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
        return web.json_response({'code': -1, 'msg': str(e)})
    return web.json_response({'code': 0, 'msg': data})


@routes.post('/%s/import' % module_name)
async def v2ray_import(request):
    data = {}
    try:
        params = await corelib.parse_param(request)
        content = params.get('text', '')
        if content:
            v2rays = v2ray_utils.update_subs(content, 'clipboard')
            urls = [item['url'] for item in v2rays]
            items = await corelib.load_items('V2ray', in_={'url': urls})
            urls = [item['url'] for item in items['items']]
            v2rays = [item for item in v2rays if item['url'] not in urls]
            corelib.save('V2ray', v2rays)
        items = await corelib.load_items('V2ray')
        # items['items'] = main.filter_fields_dict_list(items['items'], ['id', 'name', 'url', 'enable'])
        data = dict(data, **items)
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
        return web.json_response({'code': -1, 'msg': str(e)})
    return web.json_response({'code': 0, 'msg': data})


@routes.get('/%s/export/{id}' % module_name)
async def v2ray_items(request):
    data = {}
    try:
        id = request.match_info['id']
        items = await corelib.load_items('V2ray', filter={'id': id})
        if len(items['items']) > 0:
            content = v2ray_utils.render_config(
                'v2ray.json.j2', items['items'][0])
            # items['items'] = main.filter_fields_dict_list(items['items'], ['id', 'name', 'url', 'enable'])
            data['content'] = content
        else:
            data['content'] = '导出失败'
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
        data['content'] = corelib.printException(e)
    return web.json_response({'code': 0, 'msg': data})


@routes.post('/%s/test' % module_name)
async def v2ray_subs_test(request):
    data = {}
    try:
        params = await corelib.parse_param(request)
        ids = params.get('ids', [])
        items = await corelib.load_items('V2ray', in_={'id': ids})
        if len(items['items']) > 0:
            result = False
            for item in items['items']:
                item['result'], result = await v2ray_utils.test_v2ray(item)
            corelib.save('V2ray', items['items'])
        items = await corelib.load_items('V2ray')
        # items['items'] = main.filter_fields_dict_list(items['items'], ['id', 'name', 'url', 'enable'])
        data = dict(data, **items)
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
        return web.json_response({'code': -1, 'msg': str(e)})
    return web.json_response({'code': 0, 'msg': data})


@routes.post('/%s/enable' % module_name)
async def v2ray_enable(request):
    data = {}
    try:
        params = await corelib.parse_param(request)
        ids = params.get('ids', [])
        enable = params.get('enable', 1)
        if enable == 0:
            items = await corelib.load_items('V2ray', in_={'enabled': True})
            if len(items['items']) > 0:
                items = items['items']
                for item in items:
                    item['enabled'] = False
                corelib.save('V2ray', items)
            await v2ray_utils.kill_v2ray()
        if enable == 1:
            items = await corelib.load_items('V2ray', in_={'enabled': True})
            if len(items['items']) > 0:
                items = items['items']
                for item in items:
                    item['enabled'] = False
                corelib.save('V2ray', items)
            items = await corelib.load_items('V2ray', in_={'id': ids})
            if len(items['items']) > 0:
                item = items['items'][0]
                item['enabled'] = await v2ray_utils.enable_v2ray(item)
                corelib.save('V2ray', items['items'])
            else:
                return web.json_response({'code': -1, 'msg': '选择的V2ray不存在'})

        items = await corelib.load_items('V2ray')
        # items['items'] = main.filter_fields_dict_list(items['items'], ['id', 'name', 'url', 'enable'])
        data = dict(data, **items)
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
        return web.json_response({'code': -1, 'msg': str(e)})
    return web.json_response({'code': 0, 'msg': data})


@routes.get('/%s/v2ray_test' % module_name)
async def websocke_handle(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    async for msg in ws:
        if msg.type == WSMsgType.TEXT:
            if msg.data == 'close':
                logging.warning('[-]close')
                await ws.close()
            elif msg.data.startswith('v2ray_test'):
                result = {'id': -1}
                keys = json.loads(msg.data.split(' ', 1)[1])
                items = await corelib.load_items('V2ray', in_={'id': keys})
                if len(items['items']) > 0:
                    await asyncio.gather(*[v2ray_test_(item, ws)for item in items['items']])
                #     items = await asyncio.gather([v2ray_test_(item, ws)for item in items])
                #     item = items['items'][0]
                #     item['result'], item['enabled'] = await v2ray_utils.test_v2ray(item, 1080+item['id'])
                #     corelib.save('V2ray', [item])
                #     result = item
                # await ws.send_str(json.dumps(result))
                # logging.warning('v2ray_test return: %s' % result)
                await ws.close()
            else:
                await ws.send_str(msg.data + '/answer')
        elif msg.type == WSMsgType.ERROR:
            logging.error('ws connection closed with exception %s' %
                          ws.exception())
    logging.warning('websocket connection closed')
    return ws


async def v2ray_test_(item, ws):
    item['result'], result = await v2ray_utils.test_v2ray(item, 1080+int(item['id'])*2)
    corelib.save('V2ray', [item])
    await ws.send_str(json.dumps(item))
    logging.warning(f'v2ray_test return: {item}, {result}')
    return item
                    

@routes.post('/%s/delete' % module_name)
async def v2ray_delete(request):
    data = {}
    try:
        params = await corelib.parse_param(request)
        ids = params['ids']
        corelib.delete('V2ray', ids)
        items = await corelib.load_items('V2ray')
        data = dict(data, **items)
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
        return web.json_response({'code': -1, 'msg': str(e)})
    return web.json_response({'code': 0, 'msg': data})
