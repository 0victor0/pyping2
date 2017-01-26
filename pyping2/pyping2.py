__version__	= "2.0.0"

import subprocess
import os
import time
from pandas import DataFrame
 
class targets(object):

	def __init__(self, targets, timeout=10):
		self.targets = targets
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

	def show(self):
		for i, target in enumerate(self.targets):
			print "Target {0}:\t{1}".format(i+1, target)
		print "Local IP:\t{0}".format(self.host_local_ip)
		print "External IP:\t{0}".format(self.host_ext_ip)

	def tcpdump_start(self, interface):
		self.interface = interface
		tcpdump_file = self._filename+".pcap"
		subprocess.Popen([
			# "sudo",
			"tcpdump",
			"-i", self.interface,
			"-w", tcpdump_file],
			stdout=subprocess.PIPE)
		print "***Hit enter to continue on IPython...."

	def tcpdump_stop(self):
		os.system("pkill tcpdump")
		print "***pcap written to: "+self._filename+".pcap"

	def check(self):
		try:
			subprocess.call(["lft"])
			self.check_lft=1
		except OSError:
			print "Need to install layer four traceroute, lft"
		try:
			subprocess.call(["hping3", "-v"])
			self.check_hping3=1
		except OSError:
			print "Need to install hping3"
		try:
			subprocess.call(["curl-loader", "-h"])
			check_curl_loader = 1
		except OSError:
			print "Need to install curl-loader, openssl, libssl-dev"
			print "curl-loader: https://sourceforge.net/projects/curl-loader/files/"
		if self.check_lft == self.check_hping3 == 1:
			print "\n*** All dependencies installed."

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
				single_target
				],
				stdout=subprocess.PIPE)
			results_raw_lft = call_lft.communicate()[0]
			
			for line in results_raw_lft.split("\n"):
				if "ms" in line:
					self.results_lft.append(line)
			del(results_raw_lft)
			for entry in self.results_lft:
				entry = entry.replace(" ", ",")
				entry = entry +","+time.ctime()
				entry = entry +","+single_target
				self.lft_before_df.append(entry.split(","))
		
	def report(self):
		# if len(self.lft_before_df) == 0:
		# 	print "*** You must run tests first...."
		# else:
		self.df_lft = DataFrame(self.lft_before_df)
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