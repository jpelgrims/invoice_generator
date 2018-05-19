# Invoice generator

A script that generates and e-mails invoices. It uses LaTeX to generate pdf documents from a template. I used this script to send invoices to members of my student assocation (part of my tasks as the treasurer).

## How to use

### Templating

The script uses Jinja2 for templating. The templates should be placed in the following locations:

   * "*templates/invoice/invoice.tex*" for the latex invoice template
   * "*templates/email/invoice.txt*" for the email invoice template
   * "*templates/email/reminder.txt*" for the email reminder template

### Commands

To generate invoices use the following command. If no date is given, the current date is used. 
~~~bash
invoicer.py generate [date]
~~~

To send invoices use the following command. If no date is given, the current date is used. if no users are given, all generated invoices are sent.

~~~bash
invoicer.py send [date] [user1,user2,...]
~~~

To generate *and* send invoices, use the following command.

~~~bash
invoicer.py issue
~~~

To send invoice reminders, use the following command.

~~~bash
invoicer.py remind
~~~



## Dependencies
* Python 3
* Latex (latexmk)