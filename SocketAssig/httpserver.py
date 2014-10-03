#! /usr/bin/env python
#import socket module

# TODO: if requested page is / return index.html
# TODO: create the Content-Type depending on the actual content type

from socket import *
from mimetypes import mimetypes as mtypes
serverSocket = socket(AF_INET, SOCK_STREAM)

def contentType(filename):
	ext = '.' + filename.split('.')[-1]
	mimetype = 'text/plain'
	if ext in mtypes:
		mimetype = mtypes[ext]
	return "Content-Type: " + mimetype +"\r\n\r\n"

#Prepare a sever socket
#Fill in start
serverSocket.bind(('localhost', 8080))
#Fill in end
while True:
    #Establish the connection
    serverSocket.listen(1)
    print 'Ready to serve...'
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(1024)
        filename = message.split()[1]
        print message + '\n'
        filename = filename if filename is not '/' else "/index.html"
        with open(filename[1:]) as f: 
            #Send one HTTP header line into socket
            #Fill in start
            response = """HTTP/1.1 200 Ok\r\n""" + contentType(filename)
            print response
            connectionSocket.send(response)
            #Fill in end
            #Send the content of the requested file to the client
            for line in f:
                connectionSocket.send(line)
            connectionSocket.close()
    except IOError:
        #Send response message for file not Found
        #Fill in start
        notFoundResponse = """HTTP/1.0 404 Not Found\r\n\r\n<p>404 Resource not found</p>"""
        #Fill in end
        #Close client socket
        connectionSocket.send(notFoundResponse)
        #Fill in start
        connectionSocket.close()
        #Fill in end
        pass
serverSocket.close()