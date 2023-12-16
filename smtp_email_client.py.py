from socket import *
import ssl
import base64


msg = "\r\n I love computer networks!" 
endmsg = "\r\n.\r\n"

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = 'smtp-mail.outlook.com'
mailport = 587

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, mailport))

recv_response = clientSocket.recv(1024).decode()
print(recv_response)
if recv_response[:3] != '220': print('220 reply not received from server.')

# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv_helo = clientSocket.recv(1024).decode()
print(recv_helo)
if recv_helo[:3] != '250': print('250 reply not received from server.')

# Get Email Information and encode it
email = input("Enter Your Email Address")  # Input statement for email address
password = input("Enter Your Email Password")  # Input statement for email password
email_encoded = (email).encode()
password_encoded = (password).encode()
encoded_user64 = base64.b64encode(email_encoded)
encoded_pass64 = base64.b64encode(password_encoded)

# STARTTLS command to upgrade from an unsecure to a secure connection
starttls_command = "STARTTLS\r\n"
clientSocket.send(starttls_command.encode())
recv_starttls = clientSocket.recv(1024)
recv_starttls = recv_starttls.decode()
# Printing the STARTTLS command
print("STARTTLS command: " + recv_starttls)
if recv_starttls[:3] != '220': print('220 reply not received from server.')

# Wraps client socket in SSL and establishes connection
SSLClientSocket = ssl.wrap_socket(clientSocket)
# Send the hello command from the server
SSLClientSocket.send(heloCommand.encode())
# Receive the response from the server
recv_helo_ssl = SSLClientSocket.recv(1024)
recv_helo_ssl = recv_helo_ssl.decode()
# Prints messages if failed/passed
print("HELO: " + recv_helo_ssl)
if recv_helo_ssl[:3] != '250': print('250 reply not received from server.')

# Authentication Messages
authMessage = "AUTH LOGIN\r\n"
SSLClientSocket.send(authMessage.encode())  # Encodes data
recv_auth = SSLClientSocket.recv(1024).decode()  # Decodes data
# Prints messages if failed/passed
print("Authentication LOGIN: " + recv_auth)
if recv_auth[:3] != '334': print('334 reply not received from server.')

# Authenticates username and encodes it
SSLClientSocket.send(encoded_user64 + "\r\n".encode())
recv_auth_username = SSLClientSocket.recv(1024).decode()
# Prints messages if failed/passed
print("Authentication USERNAME: " + recv_auth_username)
if recv_auth_username[:3] != '334': print('334 reply not received from server.')

# Authenticates password and encodes it
SSLClientSocket.send(encoded_pass64 + "\r\n".encode())
recv_auth_password = SSLClientSocket.recv(1024).decode()
# Prints messages if failed/passed
print("Authentication PASSWORD: " + recv_auth_password)
if recv_auth_password[:3] != '235': print('235 reply not received from server.')

# Send MAIL FROM command and print server response.
mailFromCommand = f'MAIL FROM: <{email}>\r\n'
SSLClientSocket.send(mailFromCommand.encode())
recv_mail_from = SSLClientSocket.recv(1024).decode()
# Prints messages if failed/passed
print("MAIL FROM command: " + recv_mail_from)
if recv_mail_from[:3] != '250': print('250 reply not received from server')

# Send RCPT TO command and print server response.
recipient = input("Enter the recipient's email address: ")
rcptToCommand = f'RCPT TO: <{recipient}>\r\n'
SSLClientSocket.send(rcptToCommand.encode())
recv_rcpt_to = SSLClientSocket.recv(1024).decode()
# Prints messages if failed/passed
print("RCPT TO command: " + recv_rcpt_to)
if recv_rcpt_to[:3] != '250': print('250 reply not received from server.')

# Send DATA command and print server response.
dataCommand = "Data\r\n"
SSLClientSocket.send(dataCommand.encode())
recv_data = SSLClientSocket.recv(1024).decode()
# Prints messages if failed/passed
print("DATA command: " + recv_data)
if recv_data[:3] != '354': print('354 reply not received from server.')

# Send message data.
message = 'SUBJECT: Hello From Console: \r\n'

# Message ends with a single period.
SSLClientSocket.send(message.encode() + msg.encode() + endmsg.encode())
recv_message = SSLClientSocket.recv(1024).decode()
# Prints messages if failed/passed
print("Response after sending message: " + recv_message)
if recv_message[:3] != '250': print('250 reply not received from server.')

# Send QUIT command and get server response.
quitStatement = 'QUIT\r\n'
print(quitStatement)
SSLClientSocket.send(quitStatement.encode())
recv_quit = SSLClientSocket.recv(1024)
print(recv_quit)