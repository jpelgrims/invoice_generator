from invoice_generator import read_csv_data

def show_invoice_stats(date, category):
    data = read_csv_data(date, category)
    print("\nInvoices for {} ({})".format(date, category))
    print("Total value of invoices: {:.2f}\n".format(sum(sum(float(t["cost"]) for t in u) for u in data.values())))
    print("  {:<15}{:>15}".format("NAME", "TOTAL"))
    print("  " + "_"*30 + "\n")
    for user, transactions in data.items():
        print("  {:-<15}{:->15}".format(user + " ", " {:.2f}".format(sum(float(t["cost"]) for t in transactions))))