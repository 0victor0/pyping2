#PyPing2

##Intro

Pyping2 is a Python library for testing network infrastructure. There is an [accompanying Docker image](https://hub.docker.com/r/victorclark/PyPing2/) which is based on Kali Linux, which is based on Debian. If you have all the dependencies installed on your host machine, you can run PyPing2 on your host, but the image takes care of all of this for you.

##1. Dependencies

To use the library, there are dependencies for GNU/Linux and Python. [Check the Dockerfile](https://github.com/0victor0/Dockerfiles/blob/master/pyping2/Dockerfile) for more information.

##2. Using PyPing2

###Import library and instantiate PyPing2 object

Import the library and create an object by passing a list of URLs and timeout (optional, defaults to 10 seconds).

        import PyPing2
        a = PyPing2.targets(["www.pingtest.com", "www.cnn.com"])

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

###tcpdump

The library also captures packets on the network interface of your choice:

        a.tcpdump_start()

Stop capture after all tests:

        a.tcpdump_stop()

###Tests

To run tests, call the following:

        a.tests()

At the moment, this runs lft on the targets.

##3. Reporting

After the test completed, you can generate a report to `results_lft.csv`:

        a.report()

##4. Example uses

Here's what an example script would look like:

        #! /usr/bin/python

        import pyping2

        domains = ["www.pingtest.com", "www.cnn.com", "www.amazon.com"]

        a = pyping2.targets(domains)
        a.tcpdump_start()
        a.test_lft()
        a.report()
        a.tcpdump_stop()

Call your script with `sudo python yourscript.py`

##5. TODO:

More details in the TODO file (mostly Docker-related). Near term improvements:

+ hping3
+ curl-loader
+ report cleaning (currently structured, but not perfect)
+ migrate from CSV adhoc reporting to database (perhaps Docker-based)