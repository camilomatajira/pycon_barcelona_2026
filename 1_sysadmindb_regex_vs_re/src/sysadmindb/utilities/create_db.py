import log
import sqlite3
import time

con = sqlite3.connect('test.db')
cur = con.cursor()

cur.execute('''drop table logs''')
cur.execute('''CREATE TABLE logs (prival int, version int, date text, hostname text, appname text, procid int, msgid text, structureddata text, msg text, original_msg text, timestamp float)''')

original_message = "<165>1 2003-08-24T05:14:15.000003-07:00 192.0.2.1 myproc 8710 - - %% It's time to make the do-nuts."
# 
mylog = log.Log(original_message)
values = (mylog.prival, mylog.version,mylog.date, mylog.hostname, mylog.appname, mylog.procid, mylog.msgid, mylog.structureddata, mylog.msg, mylog.original_msg, time.time())
cur.execute('INSERT INTO logs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?,?,?)',values)
con.commit()

cur.execute("select * from logs")
print(cur.fetchall())
con.close()
