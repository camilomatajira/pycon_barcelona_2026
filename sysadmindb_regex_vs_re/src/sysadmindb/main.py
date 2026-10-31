import socketserver
import log
import sqlite3
import pprint
import threading
from web_server import SysadminDBHttpServer
from tcp_server import SysadminDBTcpServer


# This main, creates sysadmindb http server and tcp server which are my first implementations of the project
# Without using any dependecies outside the built-ins.
def initialize_web_server():
    server = SysadminDBHttpServer()

def initialize_tcp_server():
    server = SysadminDBTcpServer()

if __name__=='__main__':
    t1 = threading.Thread(target=initialize_web_server)
    t2 = threading.Thread(target=initialize_tcp_server)
    t1.start()
    t2.start()
