from socket import *

s = socket()
s.bind(("127.227.2.1", 5656))
s.listen(5)

c, addr = s.accept()
data = c.recv(1024 * 10)
print(data.decode())

html = "HTTP/1.1 200 OK\r\n"
html += "Content-Type:text/html\r\n"
html += "\r\n"
with open("python.html") as f:
    html += f.read()

c.send(html.encode())

c.close()
s.close()
