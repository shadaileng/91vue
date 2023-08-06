#!/usr/bin/python3
# -*- coding: utf-8 -*-

from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, Float, String, DateTime, Boolean, Text, func
)
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
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


class Porn91(db.Base, Base):
    __tablename__ = 'Porn91'

    id = Column(Integer, primary_key=True)
    path = Column(String(512), default='/root')
    name = Column(String(128))
    # -1: 暂停, 0: 下载中, 1: 下载完成
    status = Column(Integer, default=-1)
    size = Column(Integer, default=0)
    key = Column(String(128))
    uid = Column(String(128))
    uname = Column(String(128))
    url = Column(String(512))
    src = Column(String(512))
    src_local = Column(String(512))
    poster = Column(String(512))
    poster_local = Column(String(512))
    content_type = Column(String(20), default='d')
    download_count = Column(Integer)
    duration = Column(Integer, default=0)
    show = Column(Boolean, default=False)
    publish_date = Column(String(8))
    publish_stamp = Column(Float)
    created_at = Column(DateTime, default=datetime.now)
    created_date = Column(
        String(8), default=lambda: datetime.now().strftime('%Y%m%d'))
    created_stamp = Column(Float, default=lambda: datetime.now().timestamp())
    updated_at = Column(DateTime, default=datetime.now)
    updated_date = Column(
        String(8), default=lambda: datetime.now().strftime('%Y%m%d'))
    updated_stamp = Column(Float, default=lambda: datetime.now().timestamp())


class Config(db.Base, Base):
    __tablename__ = 'Config'

    id = Column(Integer, primary_key=True)
    key = Column(String(128))
    value = Column(String(4096))
    enable = Column(Boolean, default=True)
    desc = Column(String(128))
    created_at = Column(DateTime, default=datetime.now)
    created_date = Column(
        String(8), default=lambda: datetime.now().strftime('%Y%m%d'))
    created_stamp = Column(Float, default=lambda: datetime.now().timestamp())
    updated_at = Column(DateTime, default=datetime.now)
    updated_date = Column(
        String(8), default=lambda: datetime.now().strftime('%Y%m%d'))
    updated_stamp = Column(Float, default=lambda: datetime.now().timestamp())

class Downinfo(db.Base, Base):
    __tablename__ = 'Downinfo'

    id = Column(Integer, primary_key=True)
    key = Column(String(128))
    content = Column(String(14096))
    created_at = Column(DateTime, default=datetime.now)
    created_date = Column(
        String(8), default=lambda: datetime.now().strftime('%Y%m%d'))
    created_stamp = Column(Float, default=lambda: datetime.now().timestamp())
    updated_at = Column(DateTime, default=datetime.now)
    updated_date = Column(
        String(8), default=lambda: datetime.now().strftime('%Y%m%d'))
    updated_stamp = Column(Float, default=lambda: datetime.now().timestamp())


class Attachment(db.Base, Base):
    __tablename__ = 'Attachment'
    id = Column(Integer, primary_key=True)
    key = Column(String(128))
    name = Column(String(512))
    desc = Column(String(512))
    content = Column(String(14096))
    category = Column(String(128))
    status = Column(String(128))
    src = Column(String(512))
    src_local = Column(String(128))
    poster = Column(String(512))
    poster_local = Column(String(128))
    created_at = Column(DateTime, default=datetime.now)
    created_date = Column(String(8), default=lambda: datetime.now().strftime('%Y%m%d'))
    created_stamp = Column(Float, default=lambda: datetime.now().timestamp())
    updated_at = Column(DateTime, default=datetime.now)
    updated_date = Column(String(8), default=lambda: datetime.now().strftime('%Y%m%d'))
    updated_stamp = Column(Float, default=lambda: datetime.now().timestamp())


def create_session():
    return db.create_session()

if __name__ == '__main__':
    # hlsitem = [item for item in session.query(Hlsitem)]
    print('data init compelte')
