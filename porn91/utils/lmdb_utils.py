#!/usr/bin/python3
# -*- coding: utf-8 -*-
import lmdb

def init(path='lmdb_dir', max_dbs=20, map_size=1099511627776):
    env = lmdb.Environment(path, max_dbs=max_dbs, map_size=map_size)
    return env

def set(env, key, val, db=None):
    db = env.open_db(key=db)
    with env.begin(write=True) as txn:
        txn.put(str(key).encode(), val.encode(), db=db)

def get(env, key, db=None):
    val = None
    db = env.open_db(key=db)
    with env.begin(write=False) as txn:
        val = txn.get(str(key).encode(), db=db)
    return val

def delete(env, key, db=None):
    db = env.open_db(key=db)
    with env.begin(write=True) as txn:
        txn.delete(str(key).encode(), db=db)

def display(env,show=print, db=None):
    db = env.open_db(key=db)
    with env.begin(write=False) as txn:
        with txn.cursor() as cursor:
            for key, value in cursor:
                show(key, value)
