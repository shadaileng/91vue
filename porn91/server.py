#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, sys, logging, socket, time
import bencoder
import threading
import queue
from multiprocessing import Process
from utils.download import loaddata, dumpdata
from utils.daemon import CDaemon
from utils import arg_list

from aioweb import settings, logger
import porn91

# UDP 报文 buffsize
UDP_RECV_BUFFSIZE = 65535
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 1088
SLEEP_TIME = 5e-2

lock = threading.Lock()

class Server:
    def __init__(self, bind_ip, bind_port, process_id, serverdir='dist/logs/server'):
        self.bind_ip = bind_ip
        self.bind_port = bind_port
        self.process_id = process_id
        self.pid_file = f'{serverdir}/{process_id}.json'
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        # UDP 地址绑定
        self.udp.bind((self.bind_ip, self.bind_port))
        # is_alive()
        self.pool_t = queue.Queue(-1)
        self.status = True


    def run(self, flag={'status': True}):
        logging.info('[-]start server ...')
        logging.info('[-]start server %s:%s' % (self.bind_ip, self.bind_port))
        dumpdata(self.pid_file, flag)
        self.pool_t.put(threading.Thread(target=self.receive_response_forever))
        while True:
            while not self.pool_t.empty():
                task = self.pool_t.get()
                if task.is_alive(): continue
                # task.setDaemon(True)
                task.daemon=True
                task.start()
            if not self.status: break
            if lock.acquire(True):
                flag = loaddata(self.pid_file)
                lock.release()
            if not flag or not flag.get('status'): break
            time.sleep(SLEEP_TIME)

    def receive_response_forever(self):
        """
        循环接受 udp 数据
        logging.info("receive response forever {}:{}".format(self.bind_ip, self.bind_port))
        """
        # 首先加入到 DHT 网络
        # self.bootstrap()
        while True:
            try:
                # 接受返回报文
                data, address = self.udp.recvfrom(UDP_RECV_BUFFSIZE)
                # 使用 bdecode 解码返回数据
                msg = bencoder.bdecode(data)
                logging.info('[-]recv: %s' % msg)
                # 处理返回信息
                self.on_message(msg, address)
                time.sleep(SLEEP_TIME)
            except Exception as e:
                logging.warning(e)


    def on_message(self, msg, address, flag={'status': True}):
        """
        负责返回信息的处理
        :param msg: 报文信息
        :param address: 报文地址
        """
        try:
            # b"y": b"r", b"q", b"exit"
            if msg[b"y"] == b"r":
                if msg[b"r"].get(b"nodes", None):
                    self.on_find_node_response(msg)
            elif msg[b"y"] == b"q":
                if msg[b"q"] == b"task":
                    self.on_handle_task(msg, address)
                # 退出
                elif msg[b"q"] == b"exit":
                    logging.warning('[-]quit by %s:%s' % address)
                    self.status = False
                    flag['status'] = False
                    if lock.acquire(True):
                        dumpdata(self.pid_file, {'status': False})
                        lock.release()
        except KeyError:
            pass


    def on_handle_task(self, msg, address):
        '''
        msg={b'y': b'q', b'q': b'import_keys', b'import_keys': b'-p 127.0.0.1:1080 --import_keys key1 key2'}
        '''
        argv = [arg.decode('utf-8') for arg in msg[b'argv']]
        # porn91.handle_params(argv)
        if '-d' in argv:
            self.pool_t.put(threading.Thread(target=porn91.handle_params, args=(argv,False)))
        else:
            self.pool_t.put(threading.Thread(target=porn91.handle_params, args=(argv,)))


def _start_thread(offset):
    """
    启动线程
    :param offset: 端口偏移值
    """
    base_dir = settings.config['base_dir']
    serverdir = f'{base_dir}/logs/server'
    os.makedirs(serverdir, exist_ok=True)
    pid_file = f'{serverdir}/{offset}.json'
    logger.set_logger(serverdir)
    server = Server(SERVER_HOST, SERVER_PORT + offset, offset, serverdir)
    server.run()
    logging.info(f'[-]stop server {SERVER_HOST}:{SERVER_PORT + offset}')



class ClientDaemon(CDaemon):
    def __init__(self, name, save_path, stdin=os.devnull, stdout=os.devnull, stderr=os.devnull, home_dir='.', umask=0x022, verbose=1):
        super(ClientDaemon, self).__init__(save_path, stdin, stdout, stderr, home_dir, umask, verbose)
        self._name = name

    def run(self, argv):
        start_server()


def daemon(argv):
    arg_l = arg_list('-d', argv)
    if len(arg_l) <= 0 or arg_l[0] not in ['start', 'stop', 'restart', 'status', 'alive']:
        raise BaseException('[-] -d <start|stop|restart|status|alive>: %s' % arg_l)
    p_name = 'downLoad_services'
    p_dir = f'{settings.config["base_dir"]}/daemon'
    os.makedirs(p_dir, exist_ok=True)
    base_path = f'{p_dir}/{p_name}'
    cD = ClientDaemon(p_name, f'{base_path}.pid', stderr=f'{base_path}.error', stdout=f'{base_path}.log', verbose=1)
    if arg_l[0] == 'start':
        cD.start(argv)
    elif arg_l[0] == 'stop':
        cD.stop()
    elif arg_l[0] == 'restart':
        cD.restart(argv)
    elif arg_l[0] == 'alive':
        return cD.is_running()
    elif arg_l[0] == 'status':
        alive = cD.is_running()
        if alive:
            print(f'process [{cD.get_pid()}] is running ......')
        else:
            print(f'daemon process [{cD._name}] stopped')


async def _start_server(offset):
    """
    启动线程
    :param offset: 端口偏移值
    """
    base_dir = settings.config['base_dir']
    serverdir = f'{base_dir}/logs/server'
    os.makedirs(serverdir, exist_ok=True)
    pid_file = f'{serverdir}/{offset}.json'
    logger.set_logger(serverdir)
    server = Server(SERVER_HOST, SERVER_PORT + offset, offset, serverdir)
    server.run()
    logging.info(f'[-]stop server {SERVER_HOST}:{SERVER_PORT + offset}')

def start_server():
    try:
        process = Process(target=_start_thread, args=(1,))
        process.start()
        process.join()
    except KeyboardInterrupt as e:
        logging.info(f'[-] Stop: {e}')

def quit():
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    # UDP 地址绑定
    udp.bind(('127.0.0.1', SERVER_PORT - 1))

    msg = dict(
            y="q",
            q="exit",  # 指定请求为 exit
        )
    udp.sendto(bencoder.bencode(msg), ('127.0.0.1', SERVER_PORT + 1))


def send_task(argv):
    # print("send_task %s" % argv)
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    # UDP 地址绑定
    udp.bind(('127.0.0.1', SERVER_PORT - 1))

    msg = dict(
            y="q",
            q="task",
            argv=argv
        )
    udp.sendto(bencoder.bencode(msg), ('127.0.0.1', SERVER_PORT + 1))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Help: %s <start|stop|restart>' % sys.argv[0])
    if 'start' in sys.argv:
        if '-d' in sys.argv:
            daemon(['-d', 'start'])
        else:
            start_server()
    if 'stop' in sys.argv:
        quit()
    if 'restart' in sys.argv:
        quit()
        start_server()
    if 'send_task' in sys.argv:
        send_task(sys.argv)


