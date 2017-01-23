import subprocess
import os
import time
from multiprocessing import Process
import signal
from pandas import DataFrame
 
class targets(object):

	def __init__(self, targets, timeout=10):
		self.targets = targets
		self.timeout = timeout
		self.lft_before_df = []
		# proc = subprocess.Popen(["ifconfig eth0 | awk 'FNR==2{print $2}'"],
		# 	stdout=subprocess.PIPE)
		# self.host_local_ip = proc.communicate()

		# self.host_local_ip = subprocess.check_output(["ifconfig",
		# 	"eth0",
		# 	"|",
		# 	"awk",
		# 	"'FNR==2{print $2}'"])

		self.host_local_ip = subprocess.check_output("ip a show eth0 | awk 'FNR==3{print $2}'",
			shell=True)
#TODO: refactor this to remove string indexing
		self.host_local_ip = str(self.host_local_ip)[:-4]	#drop trailing new line

		self.host_ext_ip = subprocess.check_output("curl -s -X GET ipinfo.io/ip",
			shell=True)

		# self.host_local_ip = os.system("ifconfig eth0 | awk 'FNR==2{print $2}'")

	def show(self):
		for i, target in enumerate(self.targets):
			print "Target {0}:\t{1}".format(i+1, target)
		print "Local IP:\t{0}".format(self.host_local_ip)
		print "External IP:\t{0}".format(self.host_ext_ip)

	def tcpdump_start(self):
		subprocess.Popen(["sudo tcpdump",
			"-i", "eth0",
			"-w", time.strftime("%Y_%m_%d_%H\:%M\:%S")+".pcap"])
		print "***Hit enter to continue...."

#TODO: refactor this for subprocess
	def tcpdump_stop(self):
		# subprocess.Popen(["pkill", "tcpdump"])
		os.system("pkill tcpdump")

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

# TODO: make each test a that calls test_timer against each test
	def tests(self):
		self.test_lft()
		# self.test_timer(self.test_lft, self.timer)
		# self.test_lft()
		# self.test_hping3()
		# self.p1 = Process(target=self.echo)
		# self.p2 = Process(target=self.timer)
		# self.p1.start()
		# self.p2.start()

	def test_lft(self):
		'''
		Performs lft on target, saves result as a string to self.results_lft
		'''
		for single_target in self.targets:

			self.results_lft = []
			print "***Performing lft on:", single_target
			call_lft = subprocess.Popen(["sudo", "lft", single_target],
				stdout=subprocess.PIPE)
			results_raw_lft = call_lft.communicate()[0]
			# print self.results_lft
			# self.parse_test_lft(self.results_raw_lft)

	# def parse_test_lft(self, raw_results_lft):
		# for single_target in self.targets:
			
			for line in results_raw_lft.split("\n"):
				if "ms" in line:
					self.results_lft.append(line)
			del(results_raw_lft)
			for entry in self.results_lft:
				entry = entry.replace(" ", ",")
				entry = entry +","+time.ctime()
				entry = entry +","+single_target
			    # self.lft_before_df.append(time.ctime())
			    # self.lft_before_df.append(single_target)
				self.lft_before_df.append(entry.split(","))
		
	def report(self):
		self.df_lft = DataFrame(self.lft_before_df)
		self.df_lft.to_csv("results_lft.csv")
		print "***lft report generated!"

#TODO: use SIGINT or similar to kill hping3 when hangs,
# but still write result

#TODO: refactor with threading instead of timer
	def test_hping3(self):
		'''
		Performs hping3 on target, saves result as a string to self.results_hping3
		'''
		#use this to kill hping3 when it hangs:
		#subprocess.Poen().send_signal(signal.SIGINT)

		print "***Performing hping3 test on:", self.targets
		start_time=time.time()

		while time.time() < start_time + 5:
			call_hping3 = subprocess.Popen(["sudo",
				"hping3",
				"-V",
				"-S",
				self.targets,
				"-T"],
				stdout=subprocess.PIPE)
		print "***Test time out"
		# print "ps: ", os.system("ps awux | grep hping3")
		print "subprocess pid", call_hping3.pid
		os.kill(call_hping3.pid, signal.SIGSTOP)
		print signal.SIGSTOP
		# os.system("pkill hping3")
		self.results_hping3 = call_hping3.communicate()
		print self.results_hping3

	def test_curl_loader(self):
		pass

	# def echo(self):
	# 	for i in range(10):
	# 		subprocess.call(["echo", "hello"])
	# 		time.sleep(1)

#TODO: change self.p1.terminate() to signal.SIGINT ?
	def _timer(self):
		start_time = time.time()
		while True:
			# if not self.p1.is_alive(): #error - can only test a child process
			# 	self.p2.terminate()
			if time.time() - start_time > self.timeout:
				self.p1.terminate() 
				# subprocess.Popen().send_signal(signal.SIGINT)
				#self.p2.terminate()
				print "stopped the loop"
				break

	def _test_timer(self, to_check, timer):
		self.p1 = Process(target=to_check)
		self.p2 = Process(target=timer)
		self.p1.start()
		self.p2.start()

	# this is to test test_timer module
	# def try_test_timer(self):
	# 	self.test_timer(self.test_lft, self.timer)
