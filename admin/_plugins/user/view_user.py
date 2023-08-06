#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import logging
import json
import re
import hashlib
import time
import aiohttp_jinja2
from datetime import datetime
from aiohttp import web
from aioweb import corelib

from . import db
from . import main


routes = web.RouteTableDef()
module_name = 'users'


@routes.get('/%s' % module_name)
@corelib.template('user.html')
async def user_index(request):
    data = {}
    try:
        params = await corelib.parse_param(request)
        path = params.get('path', '/root')
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
    return data


@routes.get('/%s/items' % module_name)
async def user_items(request):
    data = {}
    try:
        params = await corelib.parse_param(request)
        index = int(params.get('index', '1'))
        pagesize = int(params.get('pagesize', '36'))
        session = db.create_session()
        page = await corelib.load_page('User', index, pagesize=pagesize)
        data = dict(data, **page)
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
        data['items'] = []
        data['page'] = {'page': {'total': 0, 'pages': 1, 'index': 1, 'size': pagesize}}
    return web.json_response({'code': 0, 'msg': data})


@routes.get('/%s/logininfo' % module_name)
async def user_loginIfo(request):
    data = {}
    try:
        data['now'] = None
        data['last'] = None
        data['login'] = False
        user = request.__user__
        if user:
            items = await corelib.load_items('LoginInfo', filter={'user_id': user['id']}, order_by={'id': False})
            items = items['items']
            data['login'] = True
            data['info'] = user
            data['now'] = items[0] if items is not None and len(items) > 0 else '' 
            data['last'] = items[1] if items is not None and len(items) > 1 else ''
            data['roles'] = ['admin'] if user['admin'] else []
            data['token'] = main.user2cookie(user)
            data['name'] = user['name']
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
        return web.json_response({'code': 0, 'msg': '获取失败','data': {}})
    return web.json_response({'code': 0, 'msg': '获取成功','data': data})


@routes.get('/login')
@corelib.template('login.html')
async def login(request):
    data = {}
    return data


@routes.post('/login')
async def do_login(request):
    data = {}
    try:
        params = await corelib.parse_param(request)
        name = params['name']
        password = params['password']

        user = await corelib.load_item('User', filter={'name': name})
        if not user:
            return web.json_response({'code': -1, 'field': 'name', 'msg': '请输入正确的帐号'})
        hex = hashlib.sha1(('%s:%s' % (user['name'], password)).encode('utf-8')).hexdigest()
        if user['password'] != hex:
            return web.json_response({'code': -1, 'field': 'password', 'msg': '请输入正确的密码'})
        user['login_count'] = (user['login_count'] if user['login_count'] else 0) + 1
        corelib.save(
            'LoginInfo', [{'user_id': user['id'], 'ip': request.remote}])
        corelib.save('User', [user])
        data = {'username': user['name'], 'uid': user['id'], 'email': user['email'], 'roles': ['admin'] if user['admin'] else [], 'token': main.user2cookie(user)}
        rep = web.json_response({'code': 0, 'msg': '登录成功', 'data': data})
        main.setCookie(user, rep)
        return rep
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
        return web.json_response({'code': -1, 'msg': str(e)})


@routes.get('/register')
@corelib.template('register.html')
async def register(request):
    data = {}
    return data

_RE_EMAIL = re.compile(
    r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')


@routes.post('/register')
async def do_register(request):
    try:
        params = await corelib.parse_param(request)
        name = params['name']
        email = params['email']
        password = params['password']
        if not name or not name.strip():
            return web.json_response({'code': -1, 'field': 'name', 'msg': 'name is null'})
        if not email or not _RE_EMAIL.match(email):
            return web.json_response({'code': -1, 'field': 'email', 'msg': 'email 格式不正确'})
        if not password or not _RE_SHA1.match(password):
            return web.json_response({'code': -1, 'field': 'password', 'msg': '密码格式不正确'})
        user = await corelib.load_item('User', filter={'email': email})
        if user:
            return {'code': -1, 'field': 'email', 'msg': '邮箱已注册'}
        user = {'name': name, 'password': password, 'email': email, 'admin': False}
        items = corelib.save('User', [user])
        if items is None:
            return {'code': -1, 'field': 'user', 'msg': '注册失败'}
        user = items[0].single_to_dict()
        data = {'username': user['name'], 'uid': user['id'], 'email': user['email'], 'roles': ['admin'] if user['admin'] else [], 'token': main.user2cookie(user)}
        rep = web.json_response({'code': 0, 'msg': '注册成功', 'data': data})
        main.setCookie(user, rep)
        return rep
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
        return {'code': -1, 'msg': str(e)}


@routes.get('/logout')
@corelib.template('index.html')
async def logout(request):
    data = {}
    try:
        user = request.__user__
        if user:
            loginInfo = await corelib.load_item('LoginInfo', filter={
                'user_id': user['id']}, order_by={'id': False})
            if loginInfo:
                loginInfo['logout_at'] = datetime.now()
                corelib.save('LoginInfo', [loginInfo])
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
    # rep = web.HTTPFound(location='/')
    # raise rep
    rep = web.json_response({'code': 0, 'msg': '登出成功', 'data': data})
    main.setCookie(None, rep)
    return rep


@routes.get('/records')
@corelib.template('records.html')
async def records_index(request):
    data = {}
    try:
        params = await corelib.parse_param(request)
        path = params.get('path', '/root')
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
    return data


@routes.get('/records/items')
async def records_items(request):
    data = {}
    try:
        params = await corelib.parse_param(request)
        index = int(params.get('index', '1'))
        pagesize = int(params.get('pagesize', '36') if len(params.get('pagesize', '36')) > 0 else '36')
        page = await corelib.load_page('Records', index, pagesize=pagesize, order_by={'id': False})
        data = dict(data, **page)
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
        data['items'] = []
        data['page'] = {'page': {'total': 0,
                                 'pages': 1, 'index': 1, 'size': pagesize}}
    return web.json_response({'code': 0, 'msg': data})
