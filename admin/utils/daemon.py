#!usr/bin/python3
#-*- coding: utf-8 -*-

import atexit, os, sys, time, signal

class CDaemon(object):
    def __init__(self, save_path, stdin=os.devnull, stdout=os.devnull, stderr=os.devnull, home_dir='.', umask=0x022, verbose=1):
        self._save_path = save_path
        self._stdin = stdin
        self._stdout = stdout
        self._stderr = stderr
        self._home_dir = home_dir
        self._umask = umask
        self._verbose = verbose

    def daemonize(self):
        try:
            pid = os.fork()
            if pid > 0:
                exit(0)
        except OSError as e:
            sys.stderr.write('fork #1 failed: %d (%s)\n' % (e.errno, e.strerror))
            sys.exit(1)
        if not os.path.exists(self._home_dir): os.makedirs(self._home_dir, exist_ok = True)
        os.chdir(self._home_dir)
        os.setsid()
        os.umask(self._umask)

        try:
            pid = os.fork()
            if pid > 0:
                exit(0)
        except OSError as e:
            sys.stderr.write('fork #2 failed: %d (%s)\n' % (e.errno, e.strerror))
            sys.exit(1)
        sys.stdout.flush()
        sys.stderr.flush()

        si = open(self._stdin, 'r')
        so = open(self._stdout, 'a+')

        if self._stderr:
            se = open(self._stderr, 'a+')
        else:
            se = so

        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        if self._verbose >= 1:
            print('daemon process started ...')

        atexit.register(self.del_pid)
        pid = str(os.getpid())
        open(self._save_path, 'w+').write('%s\n' % pid)

    def get_pid(self):
        try:
            pf = open(self._save_path, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
        except SystemExit:
            pid = None
        return pid
    def del_pid(self):
        print(f'remove pid file: {self._save_path}')
        if os.path.exists(self._save_path):
            os.remove(self._save_path)
    def start(self, *arg, **kw):
        if self._verbose:
            print('ready to start...')
        # if self.get_pid():
        #     msg = 'pid file %s is already exists, is running?' % self._save_path
        #     sys.stderr.write(msg)
        #     exit(1)
        self.daemonize()
        self.run(*arg, **kw)
        self.stop()

    def stop(self):
        pid = self.get_pid()
        if self._verbose:
            print(f'stoping... pid: {pid}')
        if not pid:
            msg = 'pid file [%s] does not exist. Not running?\n' % self._save_path
            sys.stderr.write(msg)
            self.del_pid()
            return
        try:
            i = 0
            self.del_pid()
            while i <= 20:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
                i = i + 1
                if i % 10 == 0:
                    os.kill(pid, signal.SIGHUP)
        except OSError as err:
            err = str(err)
            if err.find('No such process') > 0:
                self.del_pid()
            else:
                print(str(err))
                sys.exit(1)
        except BaseException as err:
            print(f'Exception: {err}')
        if self._verbose >= 1:
            print('Stopped!')
    def restart(self, *args, **kwargs):
        self.stop()
        self.start(*args, **kwargs)

    def is_running(self):
        pid = self.get_pid()
        #print(pid)
        return pid and os.path.exists('/proc/%d' % pid)

    def run(self, *args, **kwargs):
        'NOTE: override the method in subclass'
        print('base class run()')

class ClientDaemon(CDaemon):
    def __init__(self, name, save_path, stdin=os.devnull, stdout=os.devnull, stderr=os.devnull, home_dir='.', umask=0x022, verbose=1):
        super(ClientDaemon, self).__init__(save_path, stdin, stdout, stderr, home_dir, umask, verbose)
        self._name = name
    def run(self, file_out, **kw):
        fd = open(file_out, 'w')
        while True:
            line = time.ctime() + '\n'
            fd.write(line)
            fd.flush()
            time.sleep(1)
        fd.close()

if __name__ == '__main__':
    help_msg = 'Usage: python %s <start|stop|restart|status>' % sys.argv[0]
    if len(sys.argv) != 2:
        print(help_msg)
        sys.exit(1)
    p_name = 'clientd' #守护进程名称
    pid_fn = './daemon_class.pid' #守护进程pid文件的绝对路径
    log_fn = './daemon_class.log' #守护进程日志文件的绝对路径
    err_fn = './daemon_class.err.log' #守护进程启动过程中的错误日志,内部出错能从这里看到
    cD = ClientDaemon(p_name, pid_fn, stderr=err_fn, verbose=1)

    if sys.argv[1] == 'start':
        cD.start(log_fn)
    elif sys.argv[1] == 'stop':
        cD.stop()
    elif sys.argv[1] == 'restart':
        cD.restart(log_fn)
    elif sys.argv[1] == 'status':
        alive = cD.is_running()
        if alive:
            print('process [%s] is running ......' % cD.get_pid())
        else:
            print('daemon process [%s] stopped' %cD._name)
    else:
        print('invalid argument!')
        print(help_msg)

