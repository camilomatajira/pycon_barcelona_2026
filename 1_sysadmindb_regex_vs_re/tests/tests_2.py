import sys

sys.path.append("./src")
from sysadmindb import log
import sysadmindb_rs


class TestMessage:
    def test_match_only_python(self, benchmark):
        original_message = "<34>1 2003-10-11T22:14:15.003Z mymachine.example.com su - ID47 - BOM'su root' failed for lonvick on /dev/pts/8"
        benchmark(lambda: bool(log.Log.regex.match(original_message)))
