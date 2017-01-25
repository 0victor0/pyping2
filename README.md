#pyping2

Pyping2 is a Python library for performing network analysis. There is an [accompanying Docker image](https://hub.docker.com/r/victorclark/pyping2/) which is based on Debian. If you have all the dependencies installed on your host machine, you can run pyping2 on your host, but the image takes care of all of this for you.

Below is a quickstart, check the wiki for more information:

##Quickstart

An overview of the workflow:

        import pyping2
        a = pyping2.targets(["www.pingtest.com", "www.cnn.com"])
        a.tcpdump_start()
        a.tests()
        a.report()
        a.tcpdump_stop()

At this point, a CSV of test results and pcaps will be written to a timestamped directory under `pyping2_results/`.