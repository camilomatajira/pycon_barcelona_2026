import socketserver
from . import log
import sqlite3
import pprint
import time

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data_binary = self.request.recv(1024).strip()
        self.data_text = self.data_binary.decode("utf-8")

        con = sqlite3.connect('sysadmindb/test.db')
        cur = con.cursor()

        for log_text in self.data_text.split("\n"):
            print("Log being processed:")
            mylog = log.Log(log_text)
            values = (mylog.prival, mylog.version,mylog.date, mylog.hostname, mylog.appname, mylog.procid, mylog.msgid, mylog.structureddata, mylog.msg, mylog.original_msg, time.time())
            cur.execute("INSERT INTO logs ('prival', 'version' ,'date' ,'hostname' ,'appname' ,'procid' ,'msgid' ,'structureddata' ,'msg' ,'original_msg', 'timestamp') VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?,?)", values)
            con.commit()

        print("Finishing the connection")
        con.close()
        self.request.sendall("Received".encode())

class SysadminDBTcpServer():
    def __init__(self):
        HOST, PORT = "localhost", 1999
        with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
            server.serve_forever()

if __name__ == "__main__":
    HOST, PORT = "localhost", 1999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()
