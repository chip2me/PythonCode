from os import system as call
from os import path
from time import sleep
import ftplib
import telnetlib
from sys import argv
from sys import exit


            # Adapter:
a_name = 0  # Name
a_ip   = 4  # IP
a_dhcp = 5  # DHCP state
moxa_ip = "192.168.4.127"  # Initial MOXA ip, should be changable through args
new_ip  = "192.168.4.126"  # Address to communicate with MOXA
TO = 5  # Timeout. If this is too small, connection will never be stablished

# IP address changes need at least 4 seconds (?) to settle
try:
	with open("ipsettle.cfg", "r") as f:
		s = f.readline().strip()
		IP_SETTLE = int(s)
except:
	IP_SETTLE = 5




# ===== CLASS : ADAPTER ======================================================
class Adapter:
	def __init__(self):
		self.file_adapter = "dat/adapterlist"
		self.file_ipname = "dat/ipname"
		self.file_dhcp = "dat/ipdhcp"


	def _get_ip_from_name(self, name):
		call("netsh interface ip show config \"" + name + \
			"\" | findstr \"IP\" >" + self.file_ipname)
		
		with open(self.file_ipname, "r") as f:
			s = f.read()
		
		return s[24:].strip()


	def _get_dhcp_from_ip(self, ip):
		call("isdhcp.exe | findstr " + ip + " >" + self.file_dhcp)

		
		with open(self.file_dhcp, "r") as f:
			l = f.readline().split(",")
		
		try:
			return l[1].strip()
		except:
			# Asume that, for some reason, dhcp state is not available, return
			# -1 so we can know if it failed.
			return -1


	def do_set_ip(self, adapter):
		call("netsh interface ip set address \"" + adapter[a_name] + \
			"\" static " + new_ip)


	def do_return_ip(self, adapter):
		if int(adapter[a_dhcp]):
			call("netsh interface ip set address \"" + adapter[a_name] + \
				"\" dhcp")
		else:
			call("netsh interface ip set address \"" + adapter[a_name] + \
				"\" static " + adapter[a_ip])


	def generate_adapter_list(self):
		call("getmac /v /FO csv >" + self.file_adapter) #Show names for available network adapters

		with open(self.file_adapter, "r") as f:
			adapter_list = []
			for line in f:  # Split adapterlist csv into manageble lists
				l = line.split(",")
				for i in range(len(l)):  # Strip " from all entries
					l[i] = l[i].strip("\"\r\n")

				l.append( self._get_ip_from_name(l[a_name]) )

				if l[4] != "":
					if self._get_dhcp_from_ip(l[a_ip]) != -1:
						l.append( self._get_dhcp_from_ip(l[a_ip]) )
						adapter_list.append(l)
		
		# Cleanup
		#call("del " + self.file_adapter)
		#call("del " + self.file_ipname)
		#call("del " + self.file_dhcp)

		return adapter_list

Adapter = Adapter()




# ===== CLASS : MOXA =========================================================
class Moxa:
	def _ping_moxa(self):
		errorlevel = call("ping -n 1 " + moxa_ip + " >nul")

		if errorlevel == 0:
			return True
		
		else:
			# Could not reach MOXA
			return False

			
	def _delete_files(self, shimoda_n):
		print ("Deleting comserver files ...\n")
		# comserver files will be deleted
		try:
			tn = telnetlib.Telnet(moxa_ip, 23, TO)
			tn.read_until("Moxa login:", TO)
			tn.write("root\n")
			tn.read_until("Password:", TO)
			tn.write("root\n")
			tn.read_until("root@Moxa:~#", TO)
			tn.write("rm comserver\n")
			tn.read_until("dummy", 1)  # MOXA required flush
			tn.write("rm comserver.c\n")
			tn.read_until("dummy", 1)  # MOXA required flush
			tn.close() # Close telnet for now ...
		except:
			# Connection not established
			return False

			

	def _send_files(self, shimoda_n):
		# These files will be copied from the files\general folder
		files_general = ["/root/comserver",\
		                 "/root/comserver.c",\
		                 "/etc/rc.d/rc.local",]

		# These files will be copied from the respective files\shimoadaN folder
		files_shimoda = ["/etc/network/interfaces"]

		general = "files/general"
		shimoda_n = "files/shimoda"+str(shimoda_n)
		
		try:
			session = ftplib.FTP(moxa_ip, "root", "root", timeout=TO)

			# Copy files from general
			for i in range( len(files_general) ):
				with open(general+files_general[i],"rb") as f:
					session.storbinary("STOR "+files_general[i], f)

			# Copy files from given shimoda number
			for i in range( len(files_shimoda) ):
				with open(shimoda_n+files_shimoda[i],"rb") as f:
					session.storbinary("STOR "+files_shimoda[i], f)

			session.quit()
			return True
		
		except:
			# Files not successfully copied
			return False


	def _reboot_moxa(self):
		try:
			tn = telnetlib.Telnet(moxa_ip, 23, TO)
			tn.read_until("Moxa login:", TO)
			tn.write("root\n")
			tn.read_until("Password:", TO)
			tn.write("root\n")

			tn.read_until("root@Moxa:~#", TO)
			tn.write("chmod +x comserver\n")
			tn.write("reboot\n")
			tn.read_until("dummy", 1)  # MOXA requred flush
			return True

		except:
			# Connection not established
			return False


	def setup_moxa(self, shimoda_n):
		if self._ping_moxa():
			self._delete_files(shimoda_n) #New line - delete if exist and executeable
			if not self._send_files(shimoda_n):
				return False
			if not self._reboot_moxa():
				return False
			return True
		else:
			# MOXA was not successfuly setup
			return False

Moxa = Moxa()




# ===== FUNCTION : MAIN ======================================================
def main():
	# Ask for Shimoda number first
	while 1:
		try:
			shimoda_number = input("\n"*500 + "Shimoda number: ")
			if path.isdir("files/shimoda" + str(shimoda_number)):
				break

			else:
				print "Shimoda number: " + shimoda_number + \
				      " could not be found in the files directory.\n\n" +\
				      "Press any key to return ..."
				call("pause >nul")
				continue  # Go to beginning of loop

		except:
			# Something else than a number was entered in input()
			print "Shimoda number must be a single number without text.\n\n" +\
			      "Press any key to return ..."
			call("pause >nul")


	print "Generating adapter list ..."
	adapter_list = Adapter.generate_adapter_list()
	print "\n"


	success = False

	# Adapter loop. Loops through all adapters until MOXA is reached
	for i in range(len(adapter_list)):
		print "-"*16 + "\n" +\
		      "Setting \"" + adapter_list[i][a_name] + "\" to " + new_ip + " ...."
		Adapter.do_set_ip(adapter_list[i])
		sleep(IP_SETTLE)

		print "Trying to reach MOXA and setup files ..."
		if (Moxa.setup_moxa(shimoda_number)):
			Adapter.do_return_ip(adapter_list[i])
			print "Success!"
			print "Returning " + adapter_list[i][a_name] + " to " +\
			      adapter_list[i][a_ip] + " ..."
			success = True
			break

		else:
			print "Unsuccessful"
			print "Returning " + adapter_list[i][a_name] + " to " +\
			      adapter_list[i][a_ip] + " ..."
			Adapter.do_return_ip(adapter_list[i])


	if success:
		sleep(2)
		exit(0)  # Clean exit

	else:
		print "-"*16 + "\n\n\nCould not establish connection to MOXA.\n" +\
		      "Make sure that the MOXA is reset to default.\n\n" +\
		      "Press any key to exit ..."
		call("pause >nul")
		exit(1)




# ===== FUNCTION : MAIN COMMAND LINE =========================================
def main_cl(shimoda_number, cl_ip=False, cl_new_ip=False):
	global moxa_ip, new_ip
	if cl_ip:
		moxa_ip = cl_ip

		# If no new ip has been given, make one
		if not cl_new_ip:
			# Decrease or increase new_ip by 1
			a = cl_ip.split(".")
			a[3] = int(a[3])
			if a[3] > 0: a[3]-= 1
			else: a[3]+= 1
			a[3] = str(a[3])
			new_ip = ".".join(a)
		
		else:
			new_ip = cl_new_ip


	if not path.isdir("files/shimoda" + str(shimoda_number)):
		print "Shimoda number: \"" + shimoda_number + \
		      "\" could not be found in the files directory."
		exit(1)


	print "Stand by. MOXA is being configured ..."
	adapter_list = Adapter.generate_adapter_list()

	success = False
	# Adapter loop. Loops through all adapters until MOXA is reached
	for i in range(len(adapter_list)):
		#print adapter_list[i][a_name], adapter_list[i][a_ip], new_ip DEBUG
		Adapter.do_set_ip(adapter_list[i])
		sleep(IP_SETTLE)

		if (Moxa.setup_moxa(shimoda_number)):
			Adapter.do_return_ip(adapter_list[i])
			print "Success!"
			success = True
			break

		Adapter.do_return_ip(adapter_list[i])


	if success:
		exit(0)  # Clean exit

	else:
		print "Could not establish connection to MOXA.\n" +\
		      "Make sure that the MOXA is reset to default.\n\n" +\
		      "If the problem persists, try increasing the ipsettle.cfg file."
		exit(1)




if __name__ == "__main__":
	if len(argv) == 1:  # No arguments
		main()
	if len(argv) == 2:  # If only shimoda number
		main_cl(argv[1])
	if len(argv) == 3:  # If shimoda number and ip address
		main_cl(argv[1], argv[2])
	if len(argv) == 4:  # If shimoda number, ip address and pc ip address
		main_cl(argv[1], argv[2], argv[3])
