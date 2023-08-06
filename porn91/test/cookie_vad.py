#!/usr/bin/python3
# -*- coding: utf-8 -*-

import js2py


def vad():
    vadFile = "test/v1.js"
    context = js2py.EvalJs()
    js_code = ''
    with open(vadFile, 'r', errors='ignore') as dst:
        js_code = dst.read()
    # context.execute(js_code)
    src = js2py.eval_js(js_code)
    print(src)
    
if __name__ == '__main__':
    vad()