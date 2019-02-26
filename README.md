# Invoice generator

A script that generates and e-mails invoices. It uses LaTeX to generate pdf documents from a template. I use this script to send invoices to members of my student assocation (part of my tasks as the treasurer).

## How to use

### Templating

The script uses Jinja2 for templating. The templates should be placed in the following locations:

   * "*templates/invoice/invoice.tex*" for the latex invoice template
   * "*templates/email/\*.txt*" for email templates

### Commands

To generate invoices use the following command. If no date is given, the current date is used. 
~~~bash
invoicer generate [-d --date date ]     
~~~

To send invoices use the following command. If no invoice data file (*--file*) is given, the file with the filename \<current date>.txt is used. if no users are given, all generated invoices are sent. The testrun option will only send an invoice to the given e-mail address. The *--template* flag allows the user to choose an email template.

~~~bash
invoicer send [-f (--file) csv_input_file ] [-t (--template) email_template] [-u (--users) user1 user2 ... ] [--testrun]
~~~

To generate *and* send invoices, use the following command.

~~~bash
invoicer issue [-f (--file) csv_input_file ] [-t (--template) email_template] [-u (--users) user1 user2 ... ] [--testrun]
~~~

To send a message to one or more people, use the following command (useful for sending reminders or other things):

~~~bash
invoicer message
~~~



## Dependencies
* Python 3
* Latex (latexmk)