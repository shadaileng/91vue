#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import json
from aioweb import db, corelib


def execute_sql(sql):
    results = []
    try:
        session = create_session()
        sqls = sql.split(';')
        cud = []
        retrieve = []
        for item in sqls:
            item = item.strip()
            if len(item) <= 0:
                continue
            if item.upper().startswith('SELECT'):
                retrieve.append(item)
            else:
                cud.append(item)
        for item in sqls:
            item = item.strip()
            if len(item) <= 0:
                continue
            ret = session.execute('%s;' % item)
            if item in retrieve:
                ret = [dict((zip(item.keys(), item)))
                       for item in ret.fetchall()]
                results.append(ret)
            else:
                results.append({item: 'SUCCESS'})
        if len(cud) > 0:
            session.commit()
    except BaseException as e:
        return {'status': False, 'msg': e}
    return {'status': True, 'msg': results}


def create_session():
    session = db.create_session()
    try:
        pass
    except BaseException as e:
        logging.error('\n%s' % corelib.printException(e))
    return session


if __name__ == '__main__':
    print('-' * 75)
    session = db.create_session()
    # execute_sql('drop table V2ray;')
    # db.init_db()

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", help="-s {sql}")
    parser.add_argument("--json", help="--json format json")
    parser.add_argument("-i", help="-i init")
    args = parser.parse_args()

    argv = {}
    for item in args._get_kwargs():
        if item[1] is not None:
            argv[item[0]] = item[1]
    if argv.get('s', False):
        print('sql: ' + argv['s'])
        if argv.get('json', '') == 'True':
            print(json.dumps(execute_sql(argv['s']), indent=4))
        else:
            print(execute_sql(argv['s']))
    if argv.get('i', False):
        db.init_db()
        print('init complite')
    print('-' * 75)
