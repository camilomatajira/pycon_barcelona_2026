# SysadminDB

This is a proof of concept of SysadminDB: a database for System Administrators.
The Unique Value Proposition is that SysadminDB stores logs that can be queried using unix/linux powertools such as grep, sed and awk.

In this sense, the user does not need to learn PromQL (used by Prometheus or Loki), neither has to learn Lucene (ElasticSearch), nor any other DSL. The user, mainly a System Administrator, will be able to query logs, and produce metrics and kpis using his well known command line tools.

### Version with no dependencies
See the pure_python_no_dependencies branch

## Demo -> Sending logs
Start the TCP server (listens on port 1999):
```
cd src && python3 main.py
```
Then send a log:
```
logger --server 127.0.0.1 --port 1999 -T "hello world"
```
It is also possible to forward rsyslog to sysadmindb:
```
sudo su
echo "*.* action(type=\"omfwd\" target=\"127.0.0.1\" port=\"1999\" protocol=\"tcp\")" >> /etc/rsyslog.conf
systemctl restart rsyslog
```
Check the first terminal to see logs arrive and be stored.
