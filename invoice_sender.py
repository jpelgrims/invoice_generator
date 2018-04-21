import os
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def login_server(server, port, username, password):
    server = smtplib.SMTP(server, port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username, password)
    return server

# Function that sends one specific email to one or more email addresses
def send_mail(server, from_addr, to_addrs, msg):
    if not isinstance(to_addrs, list):
        to_addrs = [to_addrs]

    for address in to_addrs:
        server.sendmail(from_addr, address, msg.as_string())

def build_mail(from_addr, to_addr, subject, message, attachment=None):
    msg = MIMEMultipart()

    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr

    # Attach plain text message to the email
    msg.attach(MIMEText(message, 'plain'))

    # Attach file to the email if required
    if attachment:
        cover_letter = MIMEApplication(open(attachment, "rb").read())
        cover_letter.add_header('Content-Disposition', 'attachment', filename=attachment)
        msg.attach(cover_letter)
    return msg

def load_accounts():
    accounts = [[item.strip() for item in line.split(",")] for line in open(os.path.join("data", "accounts.txt"))]
    accounts = [{"e-mail": account[0], 
                 "name": account[1], 
                 "family_name": account[2],
                 "system_name": account[3],
                 "amount": float(account[4])} for account in accounts]
    return accounts

def fill_template(template_file, data):
    with open(template_file) as f:
        template = f.read()
    for key, value in data.items():
        template = template.replace("$"+key, str(value))
    return template

def send_reminders(email, password, server_address, server_port):
    server = login_server(server_address, server_port, email, password)

    accounts = load_accounts()
    accounts = list(filter(lambda account: account["amount"] > 0, accounts))
    template = os.path.join("templates","e-mail","reminder.txt")
    
    for account_data in accounts:
        message = fill_template(template, account_data)
        mail = build_mail(email, account_data["e-mail"], "Openstaand bedrag", message)
        send_mail(server, email, account_data["e-mail"], mail)
        time.sleep(2)

    server.quit()

def send_invoices(email, password, server_address, server_port, invoice_date):
    server = login_server(server_address, server_port, email, password)

    accounts = load_accounts()
    template = os.path.join("..","templates","e-mail","invoice.txt")
            
    for account_data in accounts:
        message = fill_template(template, account_data)
        pdf = os.path.join("invoices", invoice_date, "invoice_" + account_data["system_name"] + "_" + invoice_date + ".pdf")
        mail = build_mail(email, account_data["e-mail"], "Factuur " + invoice_date, message, attachment=pdf)
        send_mail(server, email, account_data["e-mail"], mail)
        time.sleep(2)

    server.quit()
