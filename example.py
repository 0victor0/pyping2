#! /usr/bin/python

import pyping2

domains = ["www.pingtest.com", "www.cnn.com", "www.amazon.com"]

a = pyping2.targets(domains)
a.test_lft()
a.report()