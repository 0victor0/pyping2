#PyPing2

##Intro

Pyping2 is a Python library for testing network infrastructure. There is an
[accompanying Docker image](https://hub.docker.com/r/victorclark/PyPing2/) which
is based on Kali Linux, which is based on Debian. If you have all the
dependencies installed on your host machine, you can run PyPing2 on your host,
but the image takes care of all of this for you.

##1. Dependencies

There are both 

##2. Using PyPing2

###Import library and instantiate PyPing2 object

Import the library and create an object by passing a list of URLs and timeout (optional,
defaults to 10 seconds).

        import PyPing2
        a = PyPing2.target(["www.pingtest.com"])

###Dependency check

At any time check the dependencies on your system with the check() module:

        a.check()

Again, if you are working in a container based on the PyPing2 image, you will 
have no problem.

###Summary

At any time show a summary of the PyPing2 object with the show() module:

        a.show()
        #Target: www.someURL.com
        #Host Local IP: 10.0.1.2
        #External IP: 8.8.8.8

####lft (Layer Four Traceroute)

At the moment, you can run lft on the target:

        a.test_lft()

##3. Reporting

After the test completed, you can generate a report to `results_lft.csv`:

        a.report()

##4. Example uses

Here's what an example script would look like:

        #! /usr/bin/python

        import pyping2

        domains = ["www.pingtest.com", "www.cnn.com", "www.amazon.com"]

        a = pyping2.targets(domains)
        a.test_lft()
        a.report()

Call your script with `sudo python yourscript.py`