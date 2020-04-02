'''
Create a sample file server.
This handles the following requests:

get file: send file to a client
put file: recv file from a client
list    : list current working directory (cwd)

this is how to start the server in the terminal:
$ python server.py <port number>
'''
import socket, sys, os, signal
#importing signal is not necessary, it is simply to support the code below, which is a precaution. 

HOST_NAME = "0.0.0.0"

# message receive buffer size
BUFFER_SIZE = 64

def main():
	if len(sys.argv) < 2:
		print("wrong number of arguments. example: server.py 8888") #the user needs to enter a port number
		return

	port = int(sys.argv[1]) # sys.argv[1] is the 1st argument on the command line
	cwd  = os.getcwd() #this is part of the os module, where cwd is assigned to the working directory

	print("Starting server on host: %s, port: %s" % (HOST_NAME, port))
	print("Current working directory: %s" % (cwd))
	print("Ctrl + C to exit server\n")

	def signal_handler(sig, signal_handler):
		print("Goodbye!")
		sock.close()   # close socket at the end
		sys.exit(0)


		'''
The above code is just made for extra pre caution.  It is made
to ensure that the exit made is not abrupt and that the socket
is closed before the server is forced to stop by using the signal handler
the client will be unable to send requests 
'''

	## register SIGINT to gracefully kill server. Ignore the given signal, excuted in the main pthon thread
	signal.signal(signal.SIGINT, signal_handler)



	# create socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #INET, streaming socket. AF_INET: this is the transport mechanisim
	sock.bind((HOST_NAME, port)) #binds the address (HOST_NAME, port) to a socket.
	'''  the socket is registered with the os Kernel'''
	#socket.socket() is a function available in the socket module

	print("Successfully created socket. Waiting for clients ..\n")

	# max 3 requests to be queued as the server deals with another client, server socket
	sock.listen(3) #this is a TCP listener 

	while 1:
		# poll for clients now, accepting connections
		clientSocket, addr = sock.accept()
		print("Received connection from %s" % str(addr)) #print the IP address

		#can only receive requests upto 1024 bytes.
		request = clientSocket.recv(1024)
		request = request.decode("utf-8")   # client sends utf-8 encoded bytes, so gets decoded here
		print("Received request: %s" % (request))
		

		if request.startswith("list"):  #checks what the user is requesting
			response = handleList()

		elif request.startswith("get"):
			response = handleGet(request) #calls out the functions created above.

		elif request.startswith("put"):
			response = handlePut(request)

		else:
			response = "Bad request: " + request

		clientSocket.send(response)         # server sends utf-8 encoded bytes
		clientSocket.close() #close connection
	return 0

	'''when one interaction finished, the server loops again to start accepting a new connection
		   '''


def handleGet(request): #this function is called when the user types in 'get'
	# note: request validation is done at client.
	rs = request.split("\t")    # E.g ['get', 'test.txt'] into a list, makes it easier to access, tab to make it easier to read
	file   = rs[1] #refer to the file
	

	response = b"" #in bytes
	if not os.path.isfile(file): #checks if the file exists locally
		print("file: %s does not exist" % (file)) #message printed if file does not exist
		response = b"file does not exist on server."
		print("File too big ")

	else:
		with open(file, "rb") as f: #read the file in binary
			fileBytes = f.read()  # bytes in the file
		response = fileBytes
	return response

# return utf-8 encoded bytes of \n separated list of files in current dir.
def handleList():
	files = os.listdir(".")   # "." is current directory. os.listdir is used to list the files and folders in the directory
	resp  = "\n".join(files) # when returned, all files are in a newline, not one single line
	return resp.encode("utf-8")


def handlePut(request):
	response = ""
	# note: request validation is done at client.
	rp   = request.split("\t")
	file     = rp[1]
	filedata = rp[2]   # string representing bytes
	
	if (os.path.isfile(file)): #checks if the file exists locally
		print("file already present.")
		response = "file already present on server."
	
	else:
		#save the file if it does not exist already
		fileBytes = bytes(filedata, "utf-8")
		with open(file, 'wb') as f:
			f.write(fileBytes)

		print("file %s successfully saved" % file)
		response = "file successfully saved on server."

	return response.encode("utf-8")


# execution from command line
if __name__ == '__main__':
	main()


 
