import socket, sys, os

# message receive buffer size
BUFFER_SIZE = 64

#enter the port number, any port number of choice
#utf8 is used as a decoding method, there are many decoding methods, but this has been chosen

def getList(host, port):
	requestStr    = "list"
	responseBytes = getResponseBytes(host, port, requestStr.encode("utf-8"))
	print(responseBytes.decode("utf-8")) #decode to make it human readable
	return
''' utf-8 is the type of character interpretation that is used to decode and encode human readable tex
      , it's a way of interpreting bytes.'''


def getFile(host, port, file):
	requestStr    = "get" + "\t" + file 
	responseBytes = getResponseBytes(host, port, requestStr.encode("utf-8")) #encoding the user's request
	if os.path.getsize(file)==0:
		print ("0 sized file")
	if os.path.getsize(file)>4**9: #detects when file is a really big file , greater than 4GB
		print ("file too big")
	if len(file)>255: #255 characters is the maximum file name length for most operating systems
		print("file name too long")
	# saving bytes as sent by server
	with open(file, "wb") as f: #write file in binary. In case of non ascii characters
		f.write(responseBytes)
	print("Saved file as %s" % file) 
	return


def putFile(host, port, file):

	if not os.path.isfile(file): #os.path.isfile returns true if the file exists, thus in this statement if it is not true, a message is printed
		print("file %s does not exist." % (file)) # a place holder is used, to insert the file value
		return
	if os.path.getsize(file)==0: #detects when file is a 0 sized file 
		print ("0 sized file")
		
	if os.path.getsize(file)>4**9: #detects when file is a really big file , greater than 4GB
		print ("file too big")
	if len(file)>255:
		print("file name too long")
		
	with open(file, 'rb') as f: #'rb' is used to read file in binary. Makes sure correct translation
		fileBytes = f.read()

	reqB  = bytes("put" + "\t" + file + "\t", "utf-8") + fileBytes # note: /t is for tab
	responseBytes = getResponseBytes(host, port, reqB)
	print(responseBytes.decode("utf-8")) #decoding what's encoded 

	
##	while 1:
##		if os.path.getsize(file)==0:
##			print("0")
##			#detects when file is a 0 sized file
##			return os.stat(file).st_size
##			break
##		elif os.path.getsize(file)>4**9:
##			#detects when file is a really big file , greater than 4GB
##			print ("file too big")
##			break
##		elif len(file)>255:
##			print("file name too long")
##			break
##
##		else:
##			if not os.path.isfile(file):
##				#os.path.isfile returns true if the file exists, thus in this statement if it is not true, a message is printed
##				print("file %s does not exist." % (file)) # a place holder is used, to insert the file value
##				return
##			with open(file, 'rb') as f:
##				#'rb' is used to read file in binary. Makes sure correct translation
##				fileBytes = f.read()
##				break
##
##			reqB  = bytes("put" + "\t" + file + "\t", "utf-8") + fileBytes # note: /t is for tab
##			responseBytes = getResponseBytes(host, port, reqB)
##			print(responseBytes.decode("utf-8")) #decoding what's encoded 

#Reading and writing files do not allow unicode strings which include non ascii characters
#which is why it needs to be encoded 

# send requestByes to host on port, return response
def getResponseBytes(host, port, requestBytes):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, port)) #opens a TCP connection for the port and host

	s.send(requestBytes)

	responseBytes = b""
	while True:
		# recieve data in parts
		parts = s.recv(BUFFER_SIZE) #buffer size assigned above, packets greater than the specified size cannot be recieved
		if parts:
			responseBytes += parts
		else:
			break
	s.close()
	return responseBytes


# main entry point
def main():
	args = sys.argv
	if (len(args) < 4): #length of arguments the user enters, should be greater than 4
		print("Insufficient args. Example entries:")
		print("python client.py host.localhost 5555 put test1.txt")
		print("python client.py host.localhost 5555 get test2.txt")
		print("python client.py host.localhost 5555 list")
		return 0

	host, port, command = args[1], int(args[2]), args[3]
	if command == "put":
		if (len(args) < 5):
			print("Please supply file name for put. For e.g:")
			print("python client.py host.localhost 5678 put test1.txt")
			return 0 #file name in the folder 
		file = args[4]
		putFile(host, port, file)

	elif command == "get":
		if (len(args) < 5):
			print("Please supply file name for put. For e.g:")
			print("python client.py host.localhost 5678 get test2.txt")
			return 0
		file = args[4]
		getFile(host, port, file) #calling out the getfile function created above

	elif command == "list":
		getList(host, port)
	else:
		print("Unknown request: %s" % (command)) #place holder

if __name__ == '__main__':
	main()
