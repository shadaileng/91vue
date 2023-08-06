import logging
import os
import time

from config import settings
base_dir = settings.config['base_dir']

def log_file(log_path=None):
    # 创建写入文件的handler
    if not log_path:
        log_path = settings.config['log']['path'] if 'log' in settings.config else settings.config['base_dir']
    os.makedirs(log_path, exist_ok=True)
    log_name = log_path + '/%s.log'
    map = {logging.DEBUG: 'debug', logging.INFO: 'info', logging.WARN: 'warn', logging.ERROR: 'error'}
    fhs = []
    for level in map.keys():
        fh = logging.FileHandler(log_name % map[level], mode='a')
        fh.setLevel(level)
        # 定义日志文件输出格式
        formatter = logging.Formatter(
            "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        fh.setFormatter(formatter)
        fhs.append(fh)

    return fhs


def log_cmd():
    # 创建控制台handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    ch.setFormatter(formatter)

    return ch


def set_logger(log_path=None):
    # 创建logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    # 将logger添加到handler里面
    for fh in log_file(log_path):
        logger.addHandler(fh)
    logger.addHandler(log_cmd())
