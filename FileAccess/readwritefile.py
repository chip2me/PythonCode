# File read write api
#C:\Users\Carsten\Dropbox

def read():
	f = open('tmp/testfile.txt', 'r')
	read_data = f.read()
	print(read_data)

		
		
def write():
	f = open('tmp/testfile.txt', 'w')
	f.write('Danmark')

	
	

