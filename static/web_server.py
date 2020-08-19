"""
web server 程序
完成一个类，提供给使用者，让使用者可以快速搭建web服务，展示自己的网页
"""
from socket import *
from select import *
import re


# 2个模块 1.搭建IO并发服务 2.实现http功能
class WebServer:  # host，port，html从实例化对象导入，此处设置默认值
    def __init__(self, host='0.0.0.0', port=80, html=None):
        self.host = host
        self.port = port
        self.html = html  # 网页的根目录
        self.rlist = []
        self.wlist = []
        self.xlist = []
        self.create_socket()
        self.bind()

    def create_socket(self):
        self.sock = socket()
        self.sock.setblocking(False)  # 设置成非阻塞

    def bind(self):
        self.address = (self.host, self.port)
        self.sock.bind(self.address)

    # 启动服务开始监听客户端的连接，因为创建套接字只需要一次，因此等待连接前的流程可放在默认参数中
    def start(self):
        self.sock.listen(5)
        print("Listen the port %d" % self.port)
        # 循环监控，初始监控监听套接字
        self.rlist.append(self.sock)
        while True:
            rs, ws, xs = select(self.rlist, self.wlist, self.xlist)
            for r in rs:
                if r is self.sock:
                    connfd, addr = r.accept()
                    print("Connect from", addr)
                    connfd.setblocking(False)
                    self.rlist.append(connfd)  # 将此连接增加监控
                else:
                    # 收到http请求
                    self.handle(r)

    def handle(self, connfd):
        # 接受浏览器请求
        request = connfd.recv(1024 * 10).decode()
        # 开始解析请求 --> 获取请求内容
        pattern = "[A-Z]+\s+(?P<info>/\S*)"
        result = re.match(pattern, request)
        if result:  # 非空
            # 匹配到了请求内容
            info = result.group("info")
            print("请求内容", info)
            # 发送相应数据
            self.send_html(connfd, info)
        else:
            # 没有匹配到，认为客户端断开连接
            connfd.close()
            self.rlist.remove(connfd)
            return

    def send_html(self, connfd, info):
        # info --> 请求主页，否则具体内容
        if info == "/":
            filename = self.html + "/index.html"
        else:
            filename = self.html + info
        try:
            # 请求内容可能有图片，所以以二进制打开
            f = open(filename, "rb")
        except:
            # 文件不存在
            response = "HTTP/1.1 404 Not Found\r\n"
            response += "Content-Type:text/html\r\n"
            response += "\r\n"
            response += "<h1>Sorry...<\h1>"
            response = response.encode()
        else:
            data = f.read()
            response = "HTTP/1.1 200 OK\r\n"
            response += "Connect-Type:text/html\r\n"
            response += "Content-Length:%d\r\n" % len(data)
            response += "\r\n"
            response = response.encode() + data
        finally: # 上面所有完了之后发送
            connfd.send(response)


if __name__ == '__main__':
    httpd = WebServer(host="0.0.0.0",
                      port=8001,
                      html="./static")  # 实例化对象
    httpd.start()  # 调用类方法启动服务
