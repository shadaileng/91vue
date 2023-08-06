#!/usr/bin/python3
# -*- coding: utf-8 -*-

from aioweb.corelib import bgTask

@bgTask()
async def bg_tasks(app):
    print('background_tasks beg')
    yield
    print('background_tasks end')