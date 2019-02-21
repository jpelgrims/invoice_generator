#!/usr/bin/python3

import os
import sys
import datetime
import argparse
import configparser

from invoice_generator import read_csv_data, generate_invoices
from invoice_sender import send_invoices, send_reminders
from invoice_system import collect_invoice_data, update_from_gsheets
from invoice_stats import show_invoice_stats

current_date = datetime.date.today().strftime('%Y-%m-%d')

parser = argparse.ArgumentParser(description='Send and generate invoices.')
subparsers = parser.add_subparsers(dest='command', help='All available subcommands')

stats_parser = subparsers.add_parser('stats', help='Shows information for a specific invoice')
stats_parser.add_argument('-d', '--date', default=current_date, dest='date', help='Invoice date (yyy-mm-dd)')
stats_parser.add_argument('-c', '--category', default="poef", dest='category', help='Invoice category')


gen_parser = subparsers.add_parser('generate', help='Generate invoices')
gen_parser.add_argument('-d', '--date', default=current_date, dest='date', help='Invoice date (yyy-mm-dd)')
gen_parser.add_argument('-c', '--category', default="poef", dest='category', help='Invoice category')

msg_parser = subparsers.add_parser('message', help='Send a message', description='Sends a reminder to all given users')
msg_parser.add_argument('--testrun', dest='testrun', action='store_true', help='Triggers a test run (only a predefined user will be sent an invoice')

parent_parser = argparse.ArgumentParser(add_help=False)
parent_parser.add_argument('-d', '--date', default=current_date, dest='date', help='Invoice date (yyy-mm-dd)')
parent_parser.add_argument('-c', '--category', default="poef", dest='category', help='Invoice category')
parent_parser.add_argument('-t', '--template', default="invoice.txt", dest='email_template', help='Email template')
parent_parser.add_argument('-u', '--users', nargs='*', dest='users', help='Users that will be sent an invoice')
parent_parser.add_argument('--testrun', dest='testrun', action='store_true', help='Triggers a test run (only a predefined user will be sent an invoice')

send_parser = subparsers.add_parser('send', parents=[parent_parser], help='Send invoices')
issue_parser = subparsers.add_parser('issue', parents=[parent_parser], help='Generate and send invoices')
collect_parser = subparsers.add_parser('collect', help='Collect invoice data from s.isw')




def main(args):

    config = {}
    if os.path.exists("config.ini"):
            config = configparser.ConfigParser()
            config.read("config.ini")

    if args.command == 'generate':
        data = read_csv_data(args.date, args.category)
        generate_invoices(data, args.date, args.category)
    elif args.command == "send":
        send_invoices(config["Credentials"]["email"], config["Credentials"]["password"], config["MailServer"]["server_address"], int(config["MailServer"]["server_port"]), args.date, args.category, args.email_template, users=args.users, testrun=args.testrun)
    elif args.command == "issue":
        data = read_csv_data(args.date, args.category)
        generate_invoices(data, args.date, args.category)
        send_invoices(config["Credentials"]["email"], config["Credentials"]["password"], config["MailServer"]["server_address"], int(config["MailServer"]["server_port"]), args.date, args.category, args.email_template, users=args.users, testrun=args.testrun)
    elif args.command == "message":
        send_reminders(config["Credentials"]["email"], config["Credentials"]["password"], config["MailServer"]["server_address"], int(config["MailServer"]["server_port"]), testrun=args.testrun)
    elif args.command == "update":
        #update_from_gsheets()
        pass
    elif args.command == "collect":
        collect_invoice_data(config["Shop"]["api_address"])
        pass
    elif args.command == "stats":
        show_invoice_stats(args.date, args.category)

if __name__ == "__main__":
    arguments = parser.parse_args()
    main(arguments)