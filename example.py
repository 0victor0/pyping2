#! /usr/bin/python

import pyping2

domains = ["www.pingtest.com", "www.cnn.com", "www.amazon.com"]
interface = "eth0"

a = pyping2.Targets(domains)
a.tcpdump_start(interface)
a.tests()
a.report()
a.tcpdump_stop()