#!/usr/bin/python3
# -*- coding: utf-8 -*-

import asyncio, logging

background_tasks = set()

def task_end(feature):
    background_tasks.discard(feature)
    logging.info(f'task end: {feature}')

async def add_task(coroutine, *args, **kw):
    task = asyncio.create_task(coroutine(*args, **kw))
    # 将 task 添加到集合中，以保持强引用：
    background_tasks.add(task)
    # 为了防止 task 被永远保持强引用，而无法被垃圾回收
    # 让每个 task 在结束后将自己从集合中移除：
    task.add_done_callback(task_end)
    return task