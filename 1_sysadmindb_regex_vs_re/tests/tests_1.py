import sys

sys.path.append("./src")
from sysadmindb import log
import sysadmindb_rs


class TestMessage:
    def test_init_benchmark(self, benchmark):
        original_message = "<34>1 2003-10-11T22:14:15.003Z mymachine.example.com su - ID47 - BOM'su root' failed for lonvick on /dev/pts/8"
        benchmark(lambda: log.Log(original_message))

    def test_init_benchmark_rs(self, benchmark):
        original_message = "<34>1 2003-10-11T22:14:15.003Z mymachine.example.com su - ID47 - BOM'su root' failed for lonvick on /dev/pts/8"
        benchmark(lambda: sysadmindb_rs.Log(original_message))
