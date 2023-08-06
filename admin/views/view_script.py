#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging, asyncio, json
from aiohttp import web
from aioweb import corelib
from utils import script_exec

import main

routes = web.RouteTableDef()
module_name = 'porn91'

@routes.post('/script/execute')
async def script_run(request):
    try:
        params = await corelib.parse_param(request)
        content = params.get('content', None)
        if content is None:
            return web.json_response({'code': -1, 'msg': '未找到参数"content"'})
        logging.info(f'execute: {content[:20] + "..." if len(content) > 20 else content}')
        result = await script_exec(content)
        logging.info(result)
        if result.get('status', False):
            return web.json_response({'code': 0, 'msg': str(result.get('msg', None))})
        else:
            return web.json_response({'code': -1, 'msg': result.get('msg', None)})
    except BaseException as e:
        return web.json_response({'code': -1, 'msg': str(e)})


@routes.post('/script/import')
async def script_import(request):
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
        items_exists = await corelib.load_items('Attachment', in_={'key': keys})
        for item_ in items:
            if item_.get('key', None) is None:
                return {'code': -1, 'msg': f'key of item [{item_.get("name", "")}] is null' }
            del item_['id']
            for item in items_exists['items']:
                if item_['key'] == item['key']:
                    item_['id'] = item['id']
                    break
        # print(items)
        a = corelib.save('Attachment', items)
        # print(a)
        data = {'code': 0, 'msg': '导入成功'}
        return data
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
        return {'code': -1, 'msg': str(e)}

@routes.get('/script/items')
async def script_items(request):
    data = {}
    try:
        user = request.__user__ if hasattr(request, '__user__') else None
        params = await corelib.parse_param(request)
        index = int(params.get('index', '1'))
        pagesize = int(params.get('pagesize', '36') if len(params.get('pagesize', '36')) > 0 else '36')
        #############
        if pagesize <= 0:
            pagesize = 15
        page = await corelib.load_page("Attachment", index, pagesize=pagesize, order_by={'id': False})
        data = dict(data, **page)
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
        data = {'items': []}
    data['prefix'] = '/'
    return web.json_response({'code': 0, 'data': data})



@routes.post('/script/delete')
async def script_delete(request):
    try:
        params = await corelib.parse_param(request)
        items = params.get('items', [])
        if len(items) <= 0:
            return {'code': -1, 'field': 'items', 'msg': 'items is empty'}
        user = request.__user__ if hasattr(request, '__user__') else None
        user_id = 0
        if user:
            user_id = user['id']
        ids = [item['id'] for item in items]
        print(ids)
        corelib.delete('Attachment', ids)
        data = {'code': 0, 'msg': '删除成功'}
        return data
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
        return {'code': -1, 'msg': str(e)}
