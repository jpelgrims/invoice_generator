#!/usr/bin/python3
import sys, time, os
import os.path
import datetime
import requests

def update_from_gsheets():
        raise NotImplementedError()
        

def collect_invoice_data(address):
        requests.post(address) # Generate new invoices on s.isw shop database
        response = requests.get(address) # Retrieve invoices
        today = str(datetime.date.today())

        with open(os.path.join("data", today + "_poef.csv"), "w")as f:

                f.write("systeemnaam;item;aantal;eenheidsprijs;totaal\n")

                for account, purchases in response.json().items():
                        for purchase in purchases:
                                f.write("{};{};{};{};{}\n".format(account, purchase["name"], purchase["amount"], purchase["price"], purchase["total"]))
