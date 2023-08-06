#!/usr/bin/python3
# -*- coding: utf-8 -*-

from distutils.command.config import config
from fileinput import filename
import os, logging, sys
import time, json
import asyncio
import db
import io, tarfile, lmdb

from datetime import datetime
from sqlalchemy import func
from utils import resource_name, lmdb_utils
from aioweb import settings

base_dir = settings.config.get('base_dir', '/data')

def get_config(key, default=None):
    session = db.create_session()
    item = session.query(db.Config).filter(db.Config.key == key).first()
    return item.value if item and item.enable else default


def get_configs():
    session = db.create_session()
    items = [{'key': item.key, 'value': item.value, 'enable': item.enable, 'desc': item.desc}
             for item in session.query(db.Config)]
    return items if items else []


def dumpdatadb(data_obj, tableName):
    session = db.create_session()
    table_ = getattr(db, tableName)
    items = [item for item in session.query(table_).filter(table_.key.in_([key for key in data_obj.keys()]))]
    keys = []
    for item in items:
        keys.append(item.key)
        for key, value in data_obj[item.key].items():
            setattr(item, key, value)
        item.updated_at = datetime.now()
        item.updated_date = item.updated_at.strftime('%Y%m%d')
        item.updated_stamp = item.updated_at.timestamp()
    for key, obj in data_obj.items():
        if key in keys:
            continue
        item = table_()
        for key, value in obj.items():
            setattr(item, key, value)
        session.add(item)
    session.commit()


def loaddatadb(key, tableName, default=None):
    session = db.create_session()
    table_ = getattr(db, tableName)
    item = session.query(table_).filter(table_.key == key).first()
    return item


def delete(keys, tableName):
    session = db.create_session()
    table_ = getattr(db, tableName)
    session.query(table_).filter(table_.key.in_(
        keys)).delete(synchronize_session=False)
    session.commit()


def load_items(tableName, *, keys=[], path='/root', filter={'name': None, 'status': None}, order_by={'id': False, 'created_date': False}):
    session = db.create_session()
    table_ = getattr(db, tableName)
    # filter_ = [table_.path == path]
    filter_ = []
    if len(keys) > 0:
        filter_.append(table_.key.in_(keys))
    if filter.get('name', None):
        filter_.append(table_.name.like('%%%s%%' % filter.get('name')))
    if filter.get('status', None):
        filter_.append(table_.status == filter.get('status'))
    order_by_ = []
    for key, rev in order_by.items():
        order_by_.append(
            table_.__dict__[key].desc() if rev else table_.__dict__[key])
    items = [item for item in session.query(
        table_).filter(*filter_).order_by(*order_by_)]
    return items


async def loaditems(tableName, *, keys=[], path='/root', filter={'name': None, 'status': None}, order_by={'id': False, 'created_date': False}):
    session = db.create_session()
    table_ = getattr(db, tableName)
    # filter_ = [table_.path == path]
    filter_ = []
    if len(keys) > 0:
        filter_.append(table_.key.in_(keys))
    if filter.get('name', None):
        filter_.append(table_.name.like('%%%s%%' % filter.get('name')))
    if filter.get('status', None):
        filter_.append(table_.status == filter.get('status'))
    order_by_ = []
    for key, rev in order_by.items():
        order_by_.append(
            table_.__dict__[key].desc() if rev else table_.__dict__[key])
    items = [item for item in session.query(
        table_).filter(*filter_).order_by(*order_by_)]
    return items


async def load_page(tableName, index, *, pagesize=12, filter={'name': None, 'status': None, 'uname': None}, keys=[], order_by={'publish_date': True, 'created_date': True}, path='/root'):
    session = db.create_session()
    table_ = getattr(db, tableName)
    # filter_ = [table_.path == path]
    filter_ = []
    if len(keys) > 0:
        filter_.append(table_.key.in_(keys))
    if filter.get('name'):
        filter_.append(table_.name.like('%%%s%%' % filter.get('name')))
    if filter.get('status'):
        filter_.append(table_.status == filter.get('status'))
    if filter.get('uname'):
        filter_.append(table_.uname.like('%%%s%%' % filter.get('uname')))
    total = session.query(func.count(table_.id)).filter(*filter_).scalar()
    order_by_ = []
    for key, rev in order_by.items():
        order_by_.append(
            table_.__dict__[key].desc() if rev else table_.__dict__[key])
    items = [item.dobule_to_dict() for item in session.query(table_).filter(
        *filter_).order_by(*order_by_).offset((index - 1) * pagesize).limit(pagesize)]
    pagenum = ((total - 1) // pagesize) + 1 if pagesize > 0 else 0
    return {'page': {'total': total, 'pages': pagenum, 'index': index, 'size': pagesize}, 'items': items}




async def get_file_content(path):
    content = ''
    with open(path, 'r') as src:
        content = src.read()
    return content


async def save_file(path, content):
    with open(path, 'w') as src:
        src.write(content)


def size_filter(size):
    size = int(size)
    if size == 0:
        return 0
    if size < 1024:
        return "%.3fb" % size
    if size < 1024 * 1024:
        return "%.3fK" % (size / 1024)
    if size < 1024 * 1024 * 1024:
        return "%.3fM" % (size / 1024 / 1024)
    if size < 1024 * 1024 * 1024 * 1024:
        return "%.3fM" % (size / 1024 / 1024 / 1024)


async def run_command(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()
    result = f'[{cmd!r} exited with {proc.returncode}]\n'
    if stdout:
        result += f'[stdout]\n{stdout.decode()}'
    if stderr:
        result += f'[stderr]\n{stderr.decode()}'
    return result

def setting(key=None):
    if key is None:
        return settings.config
    else:
        if '.' in key:
            keys = key.split('.')
            configs = settings.config
            for key in keys:
                configs = configs.get(key, None)
                if configs is None: break
            return configs
        else:
            return settings.config[key]

async def tail(filename, ws):
    '''
    1. 发送后10行日志
    2. 定位到文件末尾
    3. 循环读取一行
    '''
    # size = os.path.getsize(filename)
    # print('size: %s' % size)
    if not os.path.exists(filename):
        return
    start = time.time()
    with open(filename, 'rb') as src:
        lines = src.readlines()
        for line in lines[-20:]:
            line = line.decode('utf-8').strip().strip('\n')
            await ws.send_str(line)
        lines = None
        src.seek(0, 2)
        # 30分钟断开
        i = 0
        while not ws.closed and (time.time() - start < 18):
            line = src.readline().decode('utf-8').strip().strip('\n')
            print(ws.closed, line, i)
            if len(line) > 0:
                await ws.send_str(line)
            await asyncio.sleep(.1)
            i += 1
        print(ws.closed, 'line')

def validateJSON(jsonData):
  try:
    json.loads(jsonData)
  except BaseException as err:
    return False
  return True

lmdb_path = f"{base_dir}/lmdb"
env = lmdb_utils.init(lmdb_path)


def loaddata(filename):
    try:
        item = None
        with env.begin(write=False) as txn:
            data = txn.get(filename.encode())
            if data:
                if validateJSON(data.decode()):
                    item = json.loads(data.decode())
                else:
                    item = data.decode()
        return item

        # item = loaddatadb(filename, 'Downinfo')
        # if item:
        #     return json.loads(item.content)
        # else:
        #     raise BaseException('file %s not exists' % filename)
    except KeyboardInterrupt as e:
        raise e
    except BaseException as e:
        logging.warning('[-]Error[%s]: %s' % (sys.exc_info()[2].tb_lineno, e))
    return None

def dumpdata(filename, data):
    try:
        with env.begin(write=True) as txn:
            if isinstance(data, str):
                txn.put(filename.encode(), data.encode())
            else:
                txn.put(filename.encode(), json.dumps(data).encode())
        # if isinstance(data, str):
        #     dumpdatadb({filename: {'key': filename, 'content': data}}, 'Downinfo')
        # else:
        #     dumpdatadb({filename: {'key': filename, 'content': json.dumps(data, ensure_ascii=False)}}, 'Downinfo')
        return True
    except KeyboardInterrupt as e:
        raise e
    except BaseException as e:
        logging.error('[-]Error[%s]: %s' % (sys.exc_info()[2].tb_lineno, e))
        if isinstance(e, KeyboardInterrupt): raise e
    return False


async def status_path(key, path):
    # if not src.startswith(".mp4"): src = '%s.mp4' % src.rsplit('.', 1)[0]
    item = {"total": 0, "scale": 0.00, "speed": 0, "threadNum": 0}
    path_ = os.path.join(base_dir, path)
    item_ = loaddata(path_)
    if item_:
        item = item_
    item['path'] = path
    # if os.path.exists(path_):
    #     with open(path_, 'r') as src:
    #         try:
    #             item_ = json.loads(src.read())
    #         except json.decoder.JSONDecodeError as e:
    #             item_ = item
    #         if isinstance(item_, dict):
    #             item = item_
    #             item['path'] = path
    #         else:
    #             item['exception'] = f'[{path}]content is not json'
    # else:
    #     item['exception'] = f'{path} not exists'
    #     item['path'] = path
    item['key'] = key
    return item

async def status_key(key, tableName):
    session = db.create_session()
    table_ = getattr(db, tableName)
    item = session.query(table_).filter(table_.key == key, table_.status == 0).first()
    if item is None: return
    path = f'video/{resource_name(item.src)}.status'
    return await status_path(key, path)


async def make_tarfile(items):
    if len(items) <= 0: return None
    files = []
    for item in items:
        if item['src_local'] is not None:
            files.append(item['src_local'])
            files.append('.'.join([os.path.splitext(item['src_local'])[0], 'png']))
        files.append(item['poster_local'])
    file_like_object = io.BytesIO()
    with tarfile.open(fileobj=file_like_object, mode="w:gz") as tar:
        for arcname in files:
            file_path = os.path.join(base_dir, arcname)
            tar.add(file_path, arcname=arcname)
    return {'files': files, 'data': file_like_object}

async def make_tarfile_name(items, name):
    if len(items) <= 0: return None
    files = []
    for item in items:
        if item['src_local'] is not None:
            files.append(item['src_local'])
            files.append('.'.join([os.path.splitext(item['src_local'])[0], 'png']))
        files.append(item['poster_local'])
    with tarfile.open(name, mode="w:gz") as tar:
        for arcname in files:
            file_path = os.path.join(base_dir, arcname)
            if not os.path.exists(file_path): continue
            tar.add(file_path, arcname=arcname)
    return {'files': files}
