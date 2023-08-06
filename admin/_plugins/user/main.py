#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import json
import hashlib
import time
from aioweb import corelib
from datetime import datetime

from sqlalchemy import func

from . import db

COOKIE_NAME = 'awesession'
_COOKIE_KEY = 'awesession'


def setCookie(user, rep, max_age=129600):
    if user:
        rep.set_cookie(COOKIE_NAME, user2cookie(user, max_age),
                       max_age=max_age, httponly=True)
    else:
        rep.set_cookie(COOKIE_NAME, '', max_age=0, httponly=True)

# 计算加密cookie:


def user2cookie(user, max_age=129600):
    '''
    build cookie string by: id-expires-sha1
    '''
    expires = str(int(time.time() + max_age))
    s = '%s-%s-%s-%s' % (user['id'], user['password'], expires, _COOKIE_KEY)
    L = [str(user['id']), expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
    return '-'.join(L)

def getCookie(rep):
    return rep.cookies.get(COOKIE_NAME)

async def cookie2user(request):
    '''
    Parse cookie and load user if cookie is valid.
    '''
    cookie_str = request.cookies.get(COOKIE_NAME)
    if not cookie_str:
        return None
    try:
        L = cookie_str.split('-')
        if len(L) != 3:
            return None
        uid, expires, sha1 = L
        if int(expires) < time.time():
            return None
        user = await corelib.load_item('User', filter={'id': uid})
        if user is None:
            return None
        s = '%s-%s-%s-%s' % (uid, user['password'], expires, _COOKIE_KEY)
        if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
            logging.info('invalid sha1')
            return None
        user['password'] = '******'
        return user
    except Exception as e:
        logging.exception(e)
        return None


class encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, db.User):
            return obj.single_to_dict()


def record(req, rep, handler, params, resp_data, user_id):
    corelib.save('Records', [{
        'user_id': user_id,
        'remote': req.headers.get('X-Forwarded-For', req.remote),
        'reqline': '%s %s HTTP/%s.%s' % (
            req.method, req.path_qs, req.version.major, req.version.minor),
        'reqparam': json.dumps(params),
        'reqheaders': json.dumps(
            {k: v for k, v in req.headers.items()}),
        'status': 'HTTP/%s.%s %s %s' % (req.version.major,
                                        req.version.minor, rep.status, rep.reason),
        'repheaders': json.dumps(
            {k: v for k, v in rep.headers.items()}),
        'repdata': resp_data,
        'handler': handler.__name__
    }])


if __name__ == '__main__':
    pass
