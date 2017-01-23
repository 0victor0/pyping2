#! /usr/bin/python

import pyping2

domains = ["www.pingtest.com", "www.cnn.com", "www.amazon.com"]

a = pyping2.target(domains[0])
b = pyping2.target(domains[1])
c = pyping2.target(domains[2])

all_tests = [a,b,c]

for test in all_tests:
	test.test_lft()

a.generate_lft_report()