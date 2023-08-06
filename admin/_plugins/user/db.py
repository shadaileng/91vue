#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, Float, String, DateTime, Boolean, Text, func
)

from datetime import datetime
from aioweb import db, corelib


class Base():
    created_at = Column(DateTime, default=datetime.now)
    created_date = Column(
        String(8), default=lambda: datetime.now().strftime('%Y%m%d'))
    created_stamp = Column(Float, default=lambda: datetime.now().timestamp())
    updated_at = Column(DateTime, default=datetime.now)
    updated_date = Column(
        String(8), default=lambda: datetime.now().strftime('%Y%m%d'))
    updated_stamp = Column(Float, default=lambda: datetime.now().timestamp())

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


class User(db.Base, Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    # 指定name映射到name字段; name字段为字符串类形，
    name = Column(String(64))
    email = Column(String(64))
    mobile = Column(String(20))
    password = Column(String(64))
    image = Column(String(500))
    # 是否为管理员
    admin = Column(Boolean)
    login_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)
    created_date = Column(
        String(8), default=lambda: datetime.now().strftime('%Y%m%d'))
    created_stamp = Column(Float, default=lambda: datetime.now().timestamp())
    updated_at = Column(DateTime, default=datetime.now)
    updated_date = Column(
        String(8), default=lambda: datetime.now().strftime('%Y%m%d'))
    updated_stamp = Column(Float, default=lambda: datetime.now().timestamp())


class LoginInfo(db.Base, Base):
    __tablename__ = 'LoginInfo'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    ip = Column(String(80))
    location = Column(String(512))
    token = Column(String(512))
    note = Column(String(512))
    logout_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)
    created_date = Column(
        String(8), default=lambda: datetime.now().strftime('%Y%m%d'))
    created_stamp = Column(Float, default=lambda: datetime.now().timestamp())


class Records(db.Base, Base):
    __tablename__ = 'Records'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    remote = Column(String(80))
    reqline = Column(String(1024))
    reqparam = Column(String(20480))
    reqheaders = Column(String(2048))
    status = Column(String(128))
    repheaders = Column(String(2048))
    repdata = Column(String(20480))
    handler = Column(String(64))
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

    import argparse
    parser = argparse.ArgumentParser()
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
