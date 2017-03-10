#! /usr/bin/python

import pyping2

domains = ["www.pingtest.com", "www.cnn.com", "www.amazon.com"]

a = pyping2.Targets(domains)
a.tcpdump_start("eth0")
a.tests()
a.report()
a.tcpdump_stop()