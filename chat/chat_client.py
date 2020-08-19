"""
chat room  客户端
发送请求 接收消息
"""
from socket import *
from multiprocessing import Process
import sys

# 服务器地址
ADDR = ("124.70.148.168", 8000)


# 进入聊天室
def login(sock):
    while True:
        name = input("Name:")
        # 给服务端发请求
        msg = "L " + name  # 根据协议组织消息
        sock.sendto(msg.encode(), ADDR)
        # 等待结果
        result, addr = sock.recvfrom(128)
        # 约定OK作为请求成功的标志
        if result.decode() == 'OK':
            print("进入聊天室")
            return name  # 以name登录
        else:
            print("该用户已存在")


# 接收消息
def recv_msg(sock):
    while True:
        data, addr = sock.recvfrom(1024 * 10)
        # 美化打印内容
        msg = "\n" + data.decode() + "\n发言:"
        print(msg, end="")


# 发送消息
def send_msg(sock, name):
    while True:
        try:
            content = input("发言:")
        except KeyboardInterrupt:
            content = "exit"
        # 输入exit要退出
        if content == 'exit':
            msg = "E " + name
            sock.sendto(msg.encode(), ADDR)
            sys.exit("退出聊天室")
        msg = "C %s %s" % (name, content)
        sock.sendto(msg.encode(), ADDR)


def main():
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(('0.0.0.0',55667))
    # sock.sendto("测试信息".encode(),ADDR)

    # 进入聊天室
    name = login(sock)

    # 创建子进程
    p = Process(target=recv_msg, args=(sock,))
    p.daemon = True  # 子进程随父进程退出
    p.start()
    send_msg(sock, name)  # 父进程发送消息


if __name__ == '__main__':
    main()
