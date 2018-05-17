import os
import sys
import datetime
import configparser

from invoice_generator import read_data, generate_invoices
from invoice_sender import send_invoices, send_reminders

def main(argv):

    config = {}
    if os.path.exists("config.ini"):
            config = configparser.ConfigParser()
            config.read("config.ini")

    invoice_date = datetime.date.today().strftime('%Y-%m-%d')

    if len(argv) == 2:
        try:
            datetime.datetime.strptime(argv[1], '%Y-%m-%d')
            invoice_date = argv[1]
        except:
            pass

    if argv[0] == 'generate':
        data = read_data(invoice_date)
        generate_invoices(data, invoice_date)
    elif argv[0] == "send":
        send_invoices(config["Credentials"]["email"], config["Credentials"]["password"], config["Server"]["server_address"], int(config["Server"]["server_port"]), invoice_date)
    elif argv[0] == "issue":
        data = read_data(invoice_date)
        generate_invoices(data, invoice_date)
        send_invoices(config["Credentials"]["email"], config["Credentials"]["password"], config["Server"]["server_address"], int(config["Server"]["server_port"]), invoice_date)
    elif argv[0] == "remind":
        send_reminders(config["Credentials"]["email"], config["Credentials"]["password"], config["Server"]["server_address"], int(config["Server"]["server_port"]))


if __name__ == "__main__":
   main(sys.argv[1:])