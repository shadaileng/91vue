#!/usr/bin/python3
# -*- coding: utf-8 -*-

import asyncio, logging

background_tasks = {}

def task_end(feature):
    flag = False
    key = None
    val = None
    for key, val in background_tasks.items():
        if val == feature:
            flag = True
            break
    if flag:
        logging.info(f'删除任务: {key} -> {feature}')
        background_tasks.pop(key)
    else:
        logging.info(f'任务未登记: {feature}')
    logging.info(f'task end: {feature}')

async def add_task(key, coroutine, *args, **kw):
    task = asyncio.create_task(coroutine(*args, **kw))
    # 将 task 添加到集合中，以保持强引用：
    background_tasks[key] = task
    # 为了防止 task 被永远保持强引用，而无法被垃圾回收
    # 让每个 task 在结束后将自己从集合中移除：
    task.add_done_callback(task_end)
    return task


async def stop(key):
    task = background_tasks.get(key, None)
    if task:
        cancel = task.cancel()
        logging.info(f'task[{key}] cancel: {cancel}')
    else:
        logging.warning(f'task[{key}] not found')
    return task