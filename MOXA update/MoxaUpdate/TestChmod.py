from os import system as call
from os import path
from time import sleep

import telnetlib
from sys import argv
from sys import exit
import string 


            # Adapter:
a_name = 0  # Name
a_ip   = 4  # IP
a_dhcp = 5  # DHCP state
moxa_ip = "192.168.4.127"  # Initial MOXA ip, should be changable through args
new_ip  = "192.168.4.126"  # Address to communicate with MOXA
TO = 5  # Timeout. If this is too small, connection will never be stablished

flag_comserver_x = False;	#True if comserver found and done executeble

# IP address changes need at least 4 seconds (?) to settle
try:
	with open("ipsettle.cfg", "r") as f:
		s = f.readline().strip()
		IP_SETTLE = int(s)
except:
	IP_SETTLE = 5
















































































# ===== CLASS : MOXA =========================================================
class Moxa:
	def _ping_moxa(self):
		errorlevel = call("ping -n 1 " + moxa_ip + " >nul")

		if errorlevel == 0:
			return True
		
		else:
			# Could not reach MOXA
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
		print "\nMoxa communication ..."
		try:
			print "\nInside try"
			tn = telnetlib.Telnet(moxa_ip, 23, TO)
			tn.read_until("Moxa login:", TO)
			tn.write("root\n")
			tn.read_until("Password:", TO)
			tn.write("root\n")

			tn.read_until("root@Moxa:~#", TO) #Wait for prompt
			
			print "\nWrite ls ..."
			tn.write("ls -l comserver\n") #Check comserver exist and verify execution status
	
			print "\nTesting response ...\n"
			
			response = tn.read_until("root", 1) #Read response until text "root" found, timeout 1 second.
			if 1:
				print "\nRESPONSE is:\n"
				print response
				if (response.find("x") == 4): #Char no. 4 shows if file mode is executable
					flag_comserver_x = True;
				else:
					flag_comserver_x = False;
			else:
				print "\nNO RESPONSE\n"
				return 0
			print "\n... End of response ...\n"
					





			if flag_comserver_x == True:
				print "\nEXECUTABLE XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n"

			else:
				print "\nNOT_EXE\n"
			print "\n... End of response ...\n"





					
			tn.write("chmod +x comserver\n")
			#tn.write("reboot\n")
			tn.read_until("dummy", 0)  # MOXA does not reboot without it
			return True

		except:
			# Connection not established
			return False


	def setup_moxa(self, shimoda_n):
		if self._ping_moxa():
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
	print "Trying to reach MOXA and setup files ...\n"
	print "Trying to reach MOXA and setup files ...\n"




































	print "Trying to reach MOXA and setup files ...\n"
	Moxa._reboot_moxa()
	
	























































































if __name__ == "__main__":
	if len(argv) == 1:  # No arguments
		main()
		
		
		
		
		
#root@Moxa:~# ls -l comserver
#-rwxr-xr-x    1 root     root         7892 Oct 18 21:47 comserver
#root@Moxa:~#
#root@Moxa:~#
#root@Moxa:~#
#root@Moxa:~#
#root@Moxa:~# ls -l non_file
#ls: non_file: No such file or directory
#root@Moxa:~#
#root@Moxa:~#
#root@Moxa:~#
#root@Moxa:~#		






