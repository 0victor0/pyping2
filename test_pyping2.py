import glob
import os
import pyping2
import pytest
import sys

input_domains = ["www.google.com", "www.amazon.com"]
input_interface = "eth0"

@pytest.fixture
def test_pyping2():
    return pyping2.Targets(input_domains, input_interface)

def test_inputlist(test_pyping2):
    print "pyping2 not parse URLs correctly."
    assert test_pyping2.targets_csv == input_domains

def test_interface(test_pyping2):
    assert test_pyping2.interface == input_interface, "pyping2 did not use the correct interface."

# def test_tcp_dump(test_pyping2, capsys):
#     out,err  = capsys.readouterr()

#     test_pyping2.tcpdump_start()
#     out,err  = capsys.readouterr()
#     # sys.stdout.write(out)
#     # sys.stderr.write(err)
#     test_pyping2.tcpdump_stop()
    
#     print "here is out:", out
#     print "here is err:", err
#     # assert "43" in out
#     assert 1 == 2

    # print ("hello")
    # sys.stderr.write("world\n")
    # out, err = capsys.readouterr()
    # print out, err
    # assert out == "hello\n"
    # assert err == "world\n"
    # print ("next")
    # out1, err1 = capsys.readouterr()
    # assert out1 == "next\n"


# def test_csv(test_pyping2):
#     test_pyping2.tcpdump_start()
#     test_pyping2.tests()
#     test_pyping2.report()
#     test_pyping2.tcpdump_stop()
#     test_created = max(glob.iglob('pyping2_results/*/*.csv'), key=os.path.getctime)
#     test_file_size = os.path.getsize(test_created)
#     print "\nIf failed, pyping2 did not capture enough packets. Check URLs and interface name."
#     assert test_file_size > 100