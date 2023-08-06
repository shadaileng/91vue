#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import json
from aiohttp import web, web_fileresponse
from aiohttp.web import middleware
from aioweb import corelib

from . import main


@middleware
async def middleware(request, handler):
    user = await main.cookie2user(request)
    request.__user__ = user
    # print('user middleware before')
    resp = await handler(request)
    # print('user middleware after')
    # print('-' * 20)
    # print(user)
    # print('-' * 20)
    try:
        resp_data = ''
        resp_tmp = ''
        params = await corelib.parse_param(request)
        if resp is None:
            resp = {}
        if isinstance(resp, dict):
            if user:
                resp['__user__'] = user
            if hasattr(handler, '__template__'):
                request.__template__ = getattr(handler, '__template__')
                resp_tmp = web.Response(body=request.app['__templating__'].get_template(
                    getattr(handler, '__template__')).render(**resp).encode('utf-8'))
                resp_tmp.content_type = 'text/html;charset=utf-8'
            elif hasattr(request, '__template__'):
                request.__template__ = getattr(request, '__template__')
                resp_tmp = web.Response(body=request.app['__templating__'].get_template(
                    getattr(request, '__template__')).render(**resp).encode('utf-8'))
                resp_tmp.content_type = 'text/html;charset=utf-8'
            else:
                resp_tmp = web.json_response(resp)
            resp_data = json.dumps(resp)
        elif isinstance(resp, web.Response) or isinstance(resp, web_fileresponse.FileResponse):
            resp_tmp = resp
            if resp.content_type != 'application/octet-stream':
                resp_data = resp.text
            else:
                resp_data = 'application/octet-stream'
        if not request.path_qs.startswith('/records'):
            if resp_tmp == '':
                resp_tmp = resp
            main.record(request, resp_tmp, handler, params,
                        resp_data, user.get('id', -1) if user else -1)
    except BaseException as e:
        logging.error('[ERROR]: %s' % corelib.printException(e))
        resp = web.json_response(
            {'code': -1, 'msg': 500, 'exception': repr(e)})
    return resp
