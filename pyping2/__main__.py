def autoTest(auto_input, interface="eth0"):
    a = Targets(auto_input)
    a.tcpdump_start(interface)
    a.tests()
    a.report()
    a.tcpdump_stop()

if __name__ =='__main__':
    import sys
    from pyping2 import Targets
    if len(sys.argv) == 2:
        autoTest(sys.argv[1])
    if len(sys.argv) > 2:
        autoTest(sys.argv[1], sys.argv[2])