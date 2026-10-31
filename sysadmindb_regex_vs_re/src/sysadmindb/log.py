from typing import List
import re


class Log:
    pattern = r"^<(?P<prival>[0-9]+)>(?P<version>[0-9])?\s?"
    pattern += r"(?P<date>([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]+(Z|[+-][0-9]{2}:[0-9]{2})|\w{3}\s[0-9]{2}\s[0-9]{2}:[0-9]{2}:[0-9]{2}))\s"
    pattern += r"(?P<hostname>[^\s]+)\s"
    pattern += r"(?P<appname>[^\s]+)\s?"
    pattern += r"\[?(?P<procid>[0-9-]+)?\]?\:?\s?"
    pattern += r"(?P<msgid>(-|\w{2}[0-9]{2}))?\s?"
    pattern += r"(?P<structureddata>(\[.+\]|-))?\s?(BOM)?"
    pattern += r"(?P<msg>.+)?"
    regex = re.compile(pattern)

    def __init__(self, message: str):
        # print(match)
        match = self.regex.match(message)
        try:
            self.version = int(match.group("version"))
        except:
            self.version = None
        self.prival = int(match.group("prival"))
        self.date = match.group("date")
        self.hostname = match.group("hostname")
        self.appname = match.group("appname")
        self.procid = match.group("procid")
        self.msgid = match.group("msgid")
        self.structureddata = match.group("structureddata")
        try:
            self.msg = match.group("msg")
        except:
            self.msg = ""
        self.original_msg = message

    def to_query(self):
        return (
            self.prival,
            self.version,
            self.date,
            self.hostname,
            self.appname,
            self.procid,
            self.msgid,
            self.structureddata,
            self.msg,
            self.original_msg,
        )
