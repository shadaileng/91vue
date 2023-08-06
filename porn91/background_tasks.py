#!/usr/bin/python3
# -*- coding: utf-8 -*-

import asyncio, threading

from aioweb.corelib import bgTask
from server import quit

@bgTask()
async def bg_tasks(app):
    print('background_tasks beg')
    yield
    quit()
    print('background_tasks end')