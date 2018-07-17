import datetime, os
from datetime import date, datetime
import subprocess
import time
import shutil

from jinja2 import Environment, FileSystemLoader
from invoice_sender import load_accounts

PATH = os.path.dirname(os.path.abspath(__file__))

latex_jinja_env = Environment(
	block_start_string = '\BLOCK{',
	block_end_string = '}',
	variable_start_string = '\VAR{',
	variable_end_string = '}',
	comment_start_string = '\#{',
	comment_end_string = '}',
	line_statement_prefix = '%%',
	line_comment_prefix = '%#',
	trim_blocks = True,
	autoescape = False,
	loader = FileSystemLoader(os.path.join(PATH, 'templates', 'invoice'))
)

# locale setting doesn't work
def translate_date(date):
        to_dutch = {"January": "Januari", 
                          "February": "Februari", 
                          "March": "Maart", 
                          "April": "April",
                          "May": "Mei", 
                          "June": "Juni", 
                          "July": "Juli",
                          "August": "Augustus",
                          "September": "September",
                          "October": "Oktober",
                          "November": "November",
                          "December": "December"}

        date_parts = date.split(" ")
        month = to_dutch[date_parts[1]]
        return "{} {} {}".format(date_parts[0], month, date_parts[2])

def read_data(invoice_date=None):
        if not invoice_date:
                invoice_date = date.today().strftime('%Y-%m-%d')
        
        file_path = os.path.join("data",invoice_date + ".txt")
        data = {}
        current_name = ""

        with open(file_path) as data_file: 
                for line in data_file:
                        if line.startswith("Name:"):
                                current_name = line[5:].strip()
                                if not current_name in data.keys():
                                        data[current_name] = []
                        elif current_name != "" and line != "---\n":
                                purchase = line.split(";")
                                data[current_name].append({"name": purchase[0], 
                                                        "amount": purchase[1],
                                                        "price": purchase[2], 
                                                        "cost": purchase[3]})
        return data

def generate_invoices(data, invoice_date):
        # Load invoice template
        template = ""
        with open(os.path.join("templates", "invoice", "invoice.tex")) as f:
                template = f.read()

        script_path = os.path.split(os.path.realpath(__file__))[0]

        # Make output directory if it doesn't already exist
        path = os.path.join("invoices", invoice_date)
        if not os.path.exists(path):
                        os.makedirs(path)

        # Copy necessary template files to output directory
        source_dir = os.path.join("templates","invoice")
        source = os.listdir(source_dir)
        for template_file in source:
                shutil.copy(os.path.join(source_dir,template_file),path)
        
        user_data = load_accounts()

        for user in data.keys():

                total = sum(float(entry["price"])*int(entry["amount"]) for entry in data[user])
                total = str("%.2f" % round(total,2))
                username = user_data[user]["name"] + " " + user_data[user]["family_name"]
                invoice_date_full = datetime.strptime(invoice_date,'%Y-%m-%d').strftime('%d %B %Y')
                invoice_date_full = translate_date(invoice_date_full)

                template = latex_jinja_env.get_template("invoice.tex")
                invoice = template.render(name=username, invoice_items=data[user], total=total, date=invoice_date_full)
                
                filename = "invoice_{1}_{0}".format(invoice_date, user)

                os.chdir(path)

                with open(filename + ".tex", "w") as f:
                        f.write(invoice)

                cmd = ["latexmk", 
                        "-synctex=1",
                        "-interaction=nonstopmode",
                        "-file-line-error",
                        "-pdf",
                        os.path.join(script_path, path, filename + '.tex')]

                subprocess.run(cmd)
                time.sleep(1)
                os.chdir(script_path)

        # Remove all temporary build files
        source = os.listdir(path)
        for output_file in source:
                if not output_file.endswith(".pdf"):
                        os.unlink(os.path.join(path, output_file))
