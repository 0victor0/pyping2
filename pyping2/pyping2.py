__version__	= "2.1.0"

import csv
import signal
import socket
import subprocess
import sys
import os
import time

try:
	from pandas import DataFrame
except ImportError as err:
	package_problem = str(err).split(" ")[-1]
	print "\nProblem with packages. Are you using virtualenv?"
	print "Possible problem with package: {0}".format(package_problem)
	print "Fix with: pip install {0}".format(package_problem)
	sys.exit()
 
class Targets(object):


	def __init__(self, targets_csv, interface, timeout=10):
		self.targets_csv = targets_csv
		self.interface = interface
		self.timeout = timeout
		self.lft_before_df = []
		self.host_local_ip = subprocess.check_output("ip a show eth0 | awk 'FNR==3{print $2}'",
			shell=True)
		self.host_local_ip = str(self.host_local_ip)[:-4]
		self.host_ext_ip = subprocess.check_output("curl -s -X GET ipinfo.io/ip",
			shell=True)
		self._day = time.strftime('%Y_%m_%d')
		self._results_dir = "pyping2_results/"+self._day
		self._filename = self._results_dir+"/"+time.strftime('%H_%M_%S')
		os.system("mkdir -p "+self._results_dir)

		if type(self.targets_csv) == list:
			self.targets = self.targets_csv
		else:
			with open(self.targets_csv) as csv_input:
				self.targets = []
				csv_reader = csv.reader(csv_input, delimiter=",")
				for _list in csv_reader:
					for entry in _list:
						if entry is not "":
							self.targets.append(entry.strip())

	def show(self):
		for i, target in enumerate(self.targets):
			print "Target {0}:\t{1}".format(i+1, target)
		print "Local IP:\t{0}".format(self.host_local_ip)
		print "External IP:\t{0}".format(self.host_ext_ip)

	def tcpdump_start(self):

		tcpdump_file = self._filename+".pcap"

		subprocess.Popen([
			# "sudo",
			"tcpdump",
			"-i", self.interface,
			"-w", tcpdump_file],
			stdout=subprocess.PIPE)
		
	def tcpdump_stop(self):
		os.system("pkill tcpdump")
		print "***pcap written to: "+self._filename+".pcap"

	def check(self):
		try:
			p=subprocess.check_output(["ifconfig"])
			if self.interface not in p:
			    print "\n**** tcpdump error: Try changing name of network interface. Exiting."
			    sys.exit()
		except OSError:
			print "\n***Error: Are you root?"
			sys.exit()

		try:
			subprocess.call(["lft"])
			self.check_lft=1
			print "\n***lft found. Use version 3.77 for best results: http://pwhois.org/lft/\n"
		except OSError:
			print "\n***Not found: layer four traceroute, lft:"
			print "***\tPlease install from: http://pwhois.org/lft/"
			print "***\tExiting.\n"
			self.check_lft=0
			sys.exit()

	def tests(self):
		self._test_lft()

	def _test_lft(self):
		'''
		Performs lft on target, saves result as a string to self.results_lft
		'''
		for single_target in self.targets:

			self.results_lft = []
			print "***Performing lft on:", single_target
			call_lft = subprocess.Popen([
				# "sudo",
				"lft",
				"-L",
				"256",
				"-n",
				"-h",
				single_target
				],
				stdout=subprocess.PIPE)
			results_raw_lft = call_lft.communicate()[0]
			
			for line in results_raw_lft.split("\n"):
				if line.count("ms")>1:
					self.results_lft.append(line.replace("* ", ""))
			del(results_raw_lft)
			for entry in self.results_lft:
				entry = entry.replace("  ", ",")
				entry = entry +","+time.ctime()
				entry = entry +","+single_target
				try:
					hostname = socket.gethostbyaddr(entry.split(",")[1])
					entry = entry + ","+hostname[0]
				except:
					entry = entry + ","+"hostname unknown"

				self.lft_before_df.append(entry.split(","))
		
	def report(self):
		# if len(self.lft_before_df) == 0:
		# 	print "*** You must run tests first...."
		# else:
		self.df_lft = DataFrame(self.lft_before_df,
			columns = ["hop", "ip addr", "time1 [ms]", "time2 [ms]", "date", "target", "host name"])
		self.df_lft["time1 [ms]"] = self.df_lft["time1 [ms]"].str.strip(" ms")
		self.df_lft["time2 [ms]"] = self.df_lft["time2 [ms]"].str.strip(" ms")
		# self.df_lft.to_csv("pyping2_results/"+time.strftime('%Y_%b_%d_%I_%M_%S')+"results_lft.csv")

		self.df_lft.to_csv(self._filename+"_results_lft.csv")
		print "***lft report generated: "+self._filename+".csv"

	def _test_hping3(self):
		'''
		Performs hping3 on target, saves result as a string to self.results_hping3
		'''
		pass

	def _test_curl_loader(self):
		pass