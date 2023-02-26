import datetime
import os

import psutil
import weasyprint

delim = ' | '
fields = ['rss', 'vms', 'uss', 'swap']
time_fmt = '%y/%m/%d %H:%I:%S'

font_config = weasyprint.text.fonts.FontConfiguration()
iteration = 0

def printmem():
    global iteration
    pid = os.getpid()
    mem = psutil.Process(pid).memory_full_info()
    now = datetime.datetime.now()
    print(delim.join((
        str(iteration),
        now.strftime(time_fmt),
        *[str(round(getattr(mem, field, 0) / 1000000)) + 'mb' for field in fields]
    )))
    iteration = iteration + 1

def generate_pdf(): # This is a contrived example. In our actual use-case we're rendering a Django template with context variables, so each regenerate yields a unique document
    file_template = open('pdf.html', 'r')
    template = file_template.read()
    file_template.close()

    pdf = weasyprint.HTML(
        string=template,
        encoding='utf-8'
    ).write_pdf(
        font_config=font_config,
    )

    file_output = open('pdfs/' + str(iteration) + '.pdf', 'wb')
    file_output.write(pdf)
    file_output.close()

now = datetime.datetime.now()
print(delim.join((
    ' ',
    now.strftime(time_fmt),
    *[field for field in fields]
)))
printmem()

while True:
    if input().lower() != '': # If anything other than Enter/Return is input, exit. Otherwise, generate a new PDF and then print memory usage
        break
    generate_pdf()
    printmem()
