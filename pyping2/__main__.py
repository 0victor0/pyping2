def autoTest(auto_input):
    a = Targets(auto_input)
    a.tcpdump_start("eth0")
    a.tests()
    a.report()
    a.tcpdump_stop()

if __name__ =='__main__':
    import sys
    from pyping2 import Targets
    autoTest(sys.argv[1])