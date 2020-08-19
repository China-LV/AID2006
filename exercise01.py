from select import *
from socket import *

sockfd = socket()
sockfd.bind(("0.0.0.0", 8888))
sockfd.listen(5)

# 创建pool对象
p = poll()

map = {sockfd.fileno(): sockfd}  # 字典用于查找IO对象，必须与rigister对象同步

# 准备IO进行监控
p.register(sockfd, POLLOUT)

while True:
    events = p.poll()
    for fd, event in events:
        if fd == sockfd.fileno():
            connfd, addr = map[fd].accept()
            print("Connect from", addr)
            connfd.setblocking(False)
            p.register(connfd, POLLIN)
            map[connfd.fileno()] = connfd  # 维护字典，添加监控IO
        else:
            data = map[fd].recv(1024).decode()
            if not data:
                p.unregister(fd)  # 移除监控
                map[fd].close()
                del map[fd]
                continue
            print("收到：", data)
            map[fd].send(b"OK")
