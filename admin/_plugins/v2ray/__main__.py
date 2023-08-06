#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse
import logging
from . import v2ray_utils
from aioweb import logger, corelib
log = logging.getLogger()
log.setLevel(logging.INFO)
# 将logger添加到handler里面
log.addHandler(logger.log_cmd())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--parse", help="parse <filename|text|url>",
                        action="store_true", dest="is_parse", default=False)
    parser.add_argument("-t", "--test", help="test <filename|text|url>",
                        action="store_true", dest="is_test", default=False)
    parser.add_argument("-d", "--download", help="download <url>",
                        action="store_true", dest="is_download", default=False)
    parser.add_argument("-c", "--check_v2ray", help="check v2ray process alive",
                        action="store_true", dest="is_check_v2ray", default=False)
    parser.add_argument("-k", "--kill_v2ray", help="kill v2ray process",
                        action="store_true", dest="is_kill_v2ray", default=False)
    parser.add_argument("--text", help="--text <text>")
    parser.add_argument("--filename", help="--filename <filename>")
    parser.add_argument("--url", help="--url <vemss|ss>")
    args = parser.parse_args()

    if args.is_parse:
        v2rays = ''
        if args.filename is not None:
            v2rays = v2ray_utils.update_subs_file(args.filename)
        elif args.text is not None:
            v2rays = v2ray_utils.update_subs_text(args.text)
        elif args.url is not None:
            v2rays = v2ray_utils.update_subs(args.url)
        else:
            parser.print_usage()
            parser.exit(0)
        print(v2rays)
        if args.is_test:
            print(corelib.async_run([v2ray_utils.test_v2ray(v2ray) for v2ray in v2rays]))
    if args.is_check_v2ray:
        print(corelib.async_run(v2ray_utils.check_v2ray()))
    if args.is_kill_v2ray:
        print(corelib.async_run(v2ray_utils.kill_v2ray()))
    if args.is_download:
        # if args.url:
        # _get_download_speed()
        pass
    # print(args)
    '''
    if args.is_download:
        # if args.url:
        # _get_download_speed()
        pass

    '''
