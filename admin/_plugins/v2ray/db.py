#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import json
from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, Float, String, DateTime, Boolean, Text, func
)

from datetime import datetime
from aioweb import db, corelib


class Base():
    def __repr__(self):
        # return "[User(id='%s', name='%s', email='%s', admin='%s', image='%s', created_at='%s', updated_at='%s')]" % (self.id, self.name, self.email, self.admin, self.image, self.created_at, self.updated_at)
        return "[%s%s]" % (self.__tablename__, str({c.name: getattr(self, c.name) for c in self.__table__.columns}))

    def single_to_dict(self):
        return {c.name: getattr(self, c.name).strftime("%Y-%m-%d %H:%M:%S") if isinstance(getattr(self, c.name), datetime) else getattr(self, c.name) for c in self.__table__.columns}

    # 多个对象
    def dobule_to_dict(self):
        result = {}
        for key in self.__mapper__.c.keys():
            if getattr(self, key) is not None:
                val = getattr(self, key)
                if isinstance(val, datetime):
                    result[key] = val.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    result[key] = val
            else:
                result[key] = getattr(self, key)
        return result


class Subscribe(db.Base, Base):
    __tablename__ = 'Subscribe'
    id = Column(Integer, primary_key=True)
    # 指定name映射到name字段; name字段为字符串类形，
    name = Column(String(64))
    url = Column(String(256))
    enable = Column(Boolean)
    proxy = Column(Boolean)
    desc = Column(String(500))
    created_at = Column(DateTime, default=datetime.now)
    created_date = Column(
        String(8), default=lambda: datetime.now().strftime('%Y%m%d'))
    created_stamp = Column(Float, default=lambda: datetime.now().timestamp())
    updated_at = Column(DateTime, default=datetime.now)
    updated_date = Column(
        String(8), default=lambda: datetime.now().strftime('%Y%m%d'))
    updated_stamp = Column(Float, default=lambda: datetime.now().timestamp())


class V2ray(db.Base, Base):
    __tablename__ = 'V2ray'
    id = Column(Integer, primary_key=True)
    subscribe = Column(String(128))
    url = Column(String(256))
    protocol = Column(String(32))
    address = Column(String(128))
    port = Column(Integer)
    password = Column(String(256))
    key = Column(String(36))
    aid = Column(String(64))
    security = Column(String(64))
    remarks = Column(String(128))
    network = Column(String(32))
    type = Column(String(32))
    host = Column(String(256))
    path = Column(String(500))
    tls = Column(String(8))
    allowInsecure = Column(Boolean)
    SNI = Column(String(128))
    result = Column(String(1024))
    enabled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    created_date = Column(
        String(8), default=lambda: datetime.now().strftime('%Y%m%d'))
    created_stamp = Column(Float, default=lambda: datetime.now().timestamp())
    updated_at = Column(DateTime, default=datetime.now)
    updated_date = Column(
        String(8), default=lambda: datetime.now().strftime('%Y%m%d'))
    updated_stamp = Column(Float, default=lambda: datetime.now().timestamp())


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
    if argv.get('i', False):
        db.init_db()
        print('init complite')
    print('-' * 75)
