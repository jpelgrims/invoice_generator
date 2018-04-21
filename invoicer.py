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

    invoice_date = datetime.date.today().strftime('%d-%m-%Y')

    if len(argv) == 2:
        try:
            datetime.datetime.strptime(argv[1], '%d-%m-%Y')
            invoice_date = argv[1]
        except:
            pass

    if argv[0] == 'generate':
        data = read_data(invoice_date)
        generate_invoices(data, invoice_date)
    elif argv[0] == "send":
        send_invoices(config["email"], config["password"], config["server_address"], config["server_port"], invoice_date)
    elif argv[0] == "issue":
        data = read_data(invoice_date)
        generate_invoices(data, invoice_date)
        send_invoices(config["email"], config["password"], config["server_address"], config["server_port"], invoice_date)
    elif argv[0] == "remind":
        send_reminders(config["email"], config["password"], config["server_address"], config["server_port"])


if __name__ == "__main__":
   main(sys.argv[1:])