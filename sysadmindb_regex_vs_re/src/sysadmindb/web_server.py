from subprocess import Popen, PIPE, STDOUT
import sys
import pprint
import sqlite3

from http.server import HTTPServer, BaseHTTPRequestHandler


# This is highly dangerous.
# Check the next implementation that I wrote in the django project which uses a restricted shell.
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        print("command headers",self.headers.get('command'))
        user_query = self.headers.get('command')
        result = self.execute_query(user_query)
        self.end_headers()
        self.wfile.write(result)

    def execute_query(self, command : str) -> str:
        con = sqlite3.connect('test.db')
        cur = con.cursor()

        cur.execute("select * from logs")
        appended_logs = self.append_logs(cur.fetchall())
        result = self.execute_users_command(appended_logs, command)
        for line in result.decode("utf-8").split("\n"):
            print(line)
        con.close()
        return result

    def append_logs(self, query_result: tuple) -> str:
        result = ""
        original_log_line_position = 9
        for i in query_result:
            result += i[original_log_line_position] + "\n"
        return result

    def execute_users_command(self, logs: str, users_command: str) -> str:
        p = Popen([users_command], stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
        position_of_stdout = 0
        stdout_data = p.communicate(input=logs.encode())[position_of_stdout]
        return stdout_data

class SysadminDBHttpServer():
    def __init__(self):
        with HTTPServer(('localhost', 8888), SimpleHTTPRequestHandler) as server:
            server.serve_forever()

if __name__ == "__main__":
    sysadmindb = SysadminDBHttpServer()
