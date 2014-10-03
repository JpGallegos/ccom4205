#! /usr/bin/env python

# TODO: Make this shit interactive.
# TODO: look for the encryption algorithm used for account and password...

'''Used http://linuxmeerkat.wordpress.com/2013/10/10/emailing-from-a-gmail-acount-via-telnet/ as a
reference.'''

from socket import * 
import ssl
import base64
import getpass

msg = "\r\n I love computer networks!" 
endmsg = "\r\n.\r\n"
# Choose a mail server (e.g. Google mail server) and call it mailserver 
mailserver = "smtp.gmail.com"
account = ""
password = ""

loginSuccess = False

# Create socket called clientSocket and establish a TCP connection with mailserver
#Fill in start
clientSocket = socket(AF_INET, SOCK_STREAM)
sslSocket = ssl.wrap_socket(clientSocket)
sslSocket.connect((mailserver, 465))

#Fill in end
recv = sslSocket.recv(1024)
print recv
if recv[:3] != '220':
    print '220 reply not received from server.'

# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
sslSocket.send(heloCommand)
recv1 = sslSocket.recv(1024)
print recv1
if recv1[:3] != '250':
    print '250 reply not received from server.'

authCommand = 'AUTH LOGIN\r\n'
sslSocket.send(authCommand)
recvAuth = sslSocket.recv(1024)
print recvAuth
if recvAuth[:3] != '334':
	print '334 reply not recieved from server.'
else:
	account = raw_input("Gmail Account: ")
	sslSocket.send(base64.b64encode(account) + '\r\n')
	acctRecv = sslSocket.recv(1024)
	print acctRecv
	if acctRecv[:3] != '334':
		print '334 reply not recieved from server.'
	else:
		password = getpass.getpass("Password: ")
		sslSocket.send(base64.b64encode(password) + '\r\n')
		psswRecv = sslSocket.recv(1024)
		print psswRecv
		if psswRecv[:3] != '235':
			print '235 reply not recieved from server.'
		else:
			loginSuccess = True

if loginSuccess:
	# Send MAIL FROM command and print server response.
	# Fill in start
	email_from = raw_input("MAIL FROM: ")
	mailCommand = "MAIL FROM: <" + email_from + ">\r\n" 
	sslSocket.send(mailCommand)
	mailRecv = sslSocket.recv(1024)
	print mailRecv
	print mailRecv[:3]
	if psswRecv[:3] != '250':
			print '250 reply not recieved from server.'
	# Fill in end

	# Send RCPT TO command and print server response.
	# Fill in start
	recipient = raw_input("RCPT: ")
	rcptCommand = "RCPT TO: <" + recipient + ">\r\n"
	sslSocket.send(rcptCommand)
	rcptRecv = sslSocket.recv(1024)
	print rcptRecv
	if rcptRecv[:3] != '250':
			print '250 reply not recieved from server.'
	# Fill in end

	# Send DATA command and print server response.
	# Fill in start
	dataCommand = "DATA\r\n"
	sslSocket.send(dataCommand)
	dataRecv = sslSocket.recv(1024)
	print dataRecv
	if dataRecv[:3] != '354':
			print '354 reply not recieved from server.'
	# Fill in end

	# Send message data.
	# Fill in start
	subject = raw_input("Subject: ")
	message = raw_input("Message (leave empty for a standard message): ")
	if message == "":
		message = msg
	testCommand = "Subject: " + subject + "\r\n" + message + endmsg
	sslSocket.send(testCommand)
	testRecv = sslSocket.recv(1024)
	print testRecv
	if testRecv[:3] != '250':
			print '250 reply not recieved from server.'
	# Fill in end

	# Send QUIT command and get server response.
	# Fill in start
	quitCommand = "QUIT\r\n"
	sslSocket.send(quitCommand)
	quitRecv = sslSocket.recv(1024)
	print quitRecv
	# Fill in end
sslSocket.close()