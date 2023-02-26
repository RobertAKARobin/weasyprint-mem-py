import datetime
import gc
import os
import shlex
import subprocess
import time

import psutil
import weasyprint

delim = ' | '
fields = ['rss', 'vms', 'uss', 'swap']
time_fmt = '%y/%m/%d %H:%I:%S'

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
    template = shlex.quote(template)

    escaped = shlex.quote(template)
    pdf = subprocess.Popen(f"echo {escaped} | weasyprint -e utf-8 - -", shell=True, stdout=subprocess.PIPE).stdout.read()

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
    if iteration > 50:
        break
    generate_pdf()
    printmem()
