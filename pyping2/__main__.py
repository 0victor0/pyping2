def autoTest(auto_input, interface="eth0"):
    a = Targets(auto_input, interface)
    a.tcpdump_start()
    a.tests()
    a.report()
    a.tcpdump_stop()

def pyping2_help():
    print "\nPyping2 usage:"
    print "From the CLI:"
    print "\tpython -m pyping2 <csv of URLs> <network interface (eth0 is default)>"
    print "\nExample script:"
    print "\timport pyping2"
    print '\n\tdomains = ["www.url1.com", "www.url2.com", "www.url3.com"]'
    print '\tinterface = "eth0"'
    print "\n\ta = pyping2.Targets(domains, interface)"
    print "\ta.tcpdump_start()"
    print "\ta.tests()"
    print "\ta.report()"
    print "\ta.tcpdump_stop()"
    print "\nTest results will write to a new directory in pyping2_results/"
    print "For more info: https://www.github.com/0victor0/pyping2/wiki\n"
    sys.exit()

if __name__ =='__main__':
    import sys
    from pyping2 import Targets
    if "-h" in sys.argv:
        pyping2_help()
    if len(sys.argv) == 1:
        print "Must provide CSV or list of URLs"
    if len(sys.argv) == 2:
        autoTest(sys.argv[1])
    if len(sys.argv) > 2:
        autoTest(sys.argv[1], sys.argv[2])