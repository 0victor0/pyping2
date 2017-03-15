# pyping2

pyping2 is a Python library for performing network analysis. There is an [accompanying Docker image](https://hub.docker.com/r/victorclark/pyping2/) which is based on Debian. If you have all the dependencies installed on your host machine, you can run pyping2 on your host, but the image takes care of all of this for you.

Below is a quickstart, [check the wiki for more information](https://github.com/0victor0/pyping2/wiki):

## Quickstart

### Install

After download, from the install directory, install the library with `python setup.py install`.

### From the CLI

Place all the URLs you want to test in a comma-separated values file (CSV). As of release 0.2.2, URLs are required to be in the form of `www.somedomain.com` -- no `http[s]://` or trailing `/`. If you have all the dependencies installed, you can run pyping2 from the CLI:

        python -m pyping2 [your csv of URLs] [optional: name of your network interface]

Test results, a CSV and pcap file, are written to a timestamped directory under `.pyping2_results/`. As of release 0.2.2, the CSV is not completely clean; this is a planned improvement.

### Scripted flow:

And if you prefer to write your own script, here is an example flow:

        import pyping2

        domains = ["www.pingtest.com", "www.cnn.com", "www.amazon.com"]
        interface = "eth0"

        a = pyping2.Targets(domains, interface)
        a.tcpdump_start()
        a.tests()
        a.report()
        a.tcpdump_stop()

Test results will write to `./pyping2_results/`