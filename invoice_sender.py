import os
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime

from jinja2 import Environment, FileSystemLoader

PATH = os.path.dirname(os.path.abspath(__file__))

html_jinja_env = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.path.join(PATH, 'templates', 'email')),
    trim_blocks=False)

def login_server(server, port, username, password):
    server = smtplib.SMTP(server, port, '[127.0.0.1]')
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

def load_accounts(last_update=datetime.today()):
    # Function will throw an error if last_update occurs after the date the file was last updated
    # Check last update time of file
    if last_update:
        try:
            mtime = os.path.getmtime(os.path.join("data", "accounts.txt"))
        except OSError:
            mtime = 0
        last_modified_date = datetime.fromtimestamp(mtime)
        #assert(last_update.date() <= last_modified_date.date())

    accounts = [[item.strip() for item in line.split(";")] for line in open(os.path.join("data", "accounts.txt"))]
    accounts = {account[3]: {"e-mail": account[0], 
                 "first_name": account[1], 
                 "last_name": account[2],
                 "system_name": account[3],
                 "amount": float(account[4].replace(",", "."))} for account in accounts}
    return accounts

def send_reminders(email, password, server_address, server_port, testrun=False):
    server = login_server(server_address, server_port, email, password)

    accounts = load_accounts()
    if not testrun:
        accounts = filter(lambda account: account["amount"] > 0, accounts.values())
        print(accounts)
        exit
    else:
        accounts = [accounts["Jelle P"]]

    for account_data in accounts:
        template = html_jinja_env.get_template("reminder.txt")
        message = template.render(amount=account_data["amount"], name=account_data['first_name']+" "+account_data['last_name'])
        mail = build_mail(email, account_data["e-mail"], "Openstaand bedrag", message)
        send_mail(server, email, account_data["e-mail"], mail)
        print("Reminder sent for user {}".format(account_data["system_name"]))
        time.sleep(2)

    server.quit()

def send_invoices(email, password, server_address, server_port, invoice_date, invoice_category, template, users=None, testrun=False):
    server = login_server(server_address, server_port, email, password)

    accounts_data = load_accounts()

    invoices_dir = os.path.join("invoices", invoice_date + "_" + invoice_category)

    invoices = [f for f in os.listdir(invoices_dir) if os.path.isfile(os.path.join(invoices_dir, f))]
    if users:
        invoiced_users = users
    elif testrun:
        invoiced_users = ["Jelle P"]
    else:
        invoiced_users = [invoice.split("_")[1] for invoice in invoices]

    for user in invoiced_users:

        print("Sending invoice for user {}.".format(user), end=" ")
        if user in accounts_data.keys() and accounts_data[user]["e-mail"] != "":
            account = accounts_data[user]

            template = html_jinja_env.get_template(template)
            message = template.render(amount=account["amount"], first_name=account['first_name'], last_name=account['last_name'])

            if invoice_category == 'poef':
                mail_title = "Factuur " + invoice_date + " (ISW Shop)"
            else:
                mail_title = "Factuur " + invoice_date + " (Textielbesteling)"

            pdf = os.path.join("invoices", invoice_date + "_" + invoice_category, "invoice_" + account["system_name"] + "_" + invoice_date + ".pdf")
            mail = build_mail(email, account["e-mail"], mail_title, message, attachment=pdf)
            send_mail(server, email, account["e-mail"], mail)
            print("Invoice sent.")
            time.sleep(2)
        else:
            print("Invoice for user '{}' was not sent because invoicing data could not be found.".format(user))

    server.quit()
