import datetime, os
from datetime import date
import subprocess
import time
import shutil

def read_data(invoice_date=None):
        if not invoice_date:
                invoice_date = date.today().strftime('%d-%m-%Y')
        
        file_path = os.path.join("data",invoice_date + ".txt")
        data = {}

        with open(file_path) as data_file:
                for line in data_file:
                       if line.startswith("Name:"):
                                current_name = line[5:].strip()
                                if not current_name in data.keys():
                                        data[current_name] = []
                                else:
                                        if current_name != "" and line != "---\n":
                                                purchase = line.split(";")
                                                data[current_name].append({"name": purchase[0], 
                                                                        "amount": purchase[1],
                                                                        "price": purchase[2], 
                                                                        "cost": purchase[3]})
        
        return data


def generate_invoices(data, invoice_date):
        pay_by_date = (date.today() + datetime.timedelta(days=20)).strftime('%d-%m-%Y')

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

        for user in data.keys():

                invoice = template.replace("$name", user)
                invoice = invoice.replace("$pay_by_date", pay_by_date)

                purchases = ""
                total = 0
                for entry in data[user]:
                        total += float(entry["price"])*int(entry["amount"])
                        purchases += "\hourrow{{{}}}{{{}}}{{{}}}\n".format(entry["name"], entry["amount"], entry["price"]) # Item name, Amount, cumulative cost
                
                purchases += "\hline\hline\hline"
                purchases += "{\\bf Totaal} & & & {\\bf \euro" + str("%.2f" % round(total,2)) + "} \\"

                invoice = invoice.replace("$purchases", purchases)
                
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
                time.sleep(5)
                os.chdir(script_path)

        # Remove all temporary build files
        source = os.listdir(path)
        for output_file in source:
                if not output_file.endswith(".pdf"):
                        os.unlink(os.path.join(path, output_file))
