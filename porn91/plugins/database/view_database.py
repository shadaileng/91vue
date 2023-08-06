#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import logging
import json
import time
from aiohttp import web
from aioweb import corelib

from . import db


routes = web.RouteTableDef()
module_name = 'database'


@routes.get('/%s' % module_name)
@corelib.template('database.html')
async def database_index(request):
    data = {}
    try:
        params = await corelib.parse_param(request)
        path = params.get('path', '/root')
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
    return data


@routes.post('/%s/execute' % module_name)
async def execute_sql(request):
    params = await corelib.parse_param(request)
    sql = params.get(
        'sql', "SELECT CAST('test unicode returns' AS VARCHAR(60)) AS anon_1")
    logging.info(sql)
    if sql is None or len(sql) <= 0:
        logging.error('sql 为空";": %s' % (sql))
        return {'code': -1, 'msg': 'sql 为空";": %s' % (sql)}
    # if ';' not in sql:
    #     logging.error('sql 中不包含";": %s' % (sql))
    #     return {'code': -1, 'msg': 'sql 中不包含";": %s' % (sql)}
    result = corelib.execute_sql(sql)
    if result['status']:
        return {'code': 0, 'msg': json.dumps(result['msg'], ensure_ascii=False)}
    logging.error('failed to execute_sql: %s\n%s' % (sql, result['msg']))
    return {'code': -1, 'msg': 'failed to execute_sql: %s\n%s' % (sql, result['msg'])}
