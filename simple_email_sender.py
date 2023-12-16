import smtplib # no manual SSL/TLS Handling
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

mailserver = "smtp.office365.com"  #initialize Outlook SMTP server
mailport = 587  #initialize mail port
username = input("Enter Your Email Address: ") #input for email address
password = input("Enter Your Email Password: ") #input for password

#try catch block to verify email address
try:
    #connect to SMTP server on a specified mail port
    server = smtplib.SMTP(mailserver, mailport) 
    #starttls
    server.starttls()
    server.login(username, password)

    # Compose the email
    sender_email = username
    recipient = input("Enter the recipient's email address: ") #input message for recipients email address
    subject = "This is a message" #initialize the subject of the message
    body = "I love computer networks!" #initialize the body of the message

    #message properties
    msg = MIMEMultipart()
    msg["From"] = sender_email 
    msg["To"] = recipient
    msg["Subject"] = subject

    #attatch message
    msg.attach(MIMEText(body, "plain"))

    # Send the email
    server.sendmail(sender_email, recipient, msg.as_string())

    # Quit the server
    server.quit()

    print("Email sent successfully.")#display message if email is successfull
    #error handling
except smtplib.SMTPException as e:
    #error message
    print(f"An error occurred: {e}")