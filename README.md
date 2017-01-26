#pyping2

pyping2 is a Python library for performing network analysis. There is an [accompanying Docker image](https://hub.docker.com/r/victorclark/pyping2/) which is based on Debian. If you have all the dependencies installed on your host machine, you can run pyping2 on your host, but the image takes care of all of this for you.

Below is a quickstart, check the wiki for more information:

##Quickstart

###Install

Install the library with `python setup.py install`.

###From the CLI

Place all the URLs you want to test in a comma-separated values file (CSV). If you have all the dependencies install, you can run pyping2 from the CLI:

        python -m pyping2 [location of CSV file]

Test results, a CSV and pcap file, are written to a timestamped directory under `.pyping2_results/`.

###Scripted flow:

And if you prefer to use the interpreter, here is an example flow:

        import pyping2
        a = pyping2.targets(["www.pingtest.com", "www.cnn.com"])
        a.tcpdump_start()
        a.tests()
        a.report()
        a.tcpdump_stop()

Test results will write to `./pyping2_results/`