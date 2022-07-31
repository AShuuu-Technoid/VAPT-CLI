from fileinput import filename
import os
import glob
import pdfkit
import smtplib
from email.message import EmailMessage
from datetime import date
from pathlib import Path

today = date.today()
d1 = today.strftime("%d%m%Y")

Path(".Report").mkdir(parents=True, exist_ok=True,)
Path(".Report").chmod(0o777)

EMAIL_ADDRESS = '' # Enter Email Address
EMAIL_PASSWORD = '' # Enter Email Password

msg = EmailMessage()
msg['Subject'] = f'VAPT Report for project {today.strftime("%d/%m/%Y")}'
msg['From'] = EMAIL_ADDRESS
msg['To'] = '' # Enter TO Email Address
msg.set_content(f'''Hi all,

Please find the VAPT report attachement for {today.strftime("%d/%m/%y")}.

Thanks,
DevOps Team.''')

print("Docker Running ...", end='\r', flush=True)
command = 'docker run -v $(pwd)/.Report:/zap/wrk/:rw -t owasp/zap2docker-stable zap-full-scan.py -t https://example.com -g gen.conf -r $(date +"%Y%m%d").html >/dev/null 2>&1'
p = os.system(command)
print("Docker Completed ...", end='', flush=True)
print()
print("Report Generating ...", end='\r', flush=True)

list_of_html_files = glob.glob('.Report/*.html')
latest_file_html = max(list_of_html_files, key=os.path.getctime)

pdf_filename = (f".Report/proj-{d1}.pdf")

pdfkit.from_file(latest_file_html, pdf_filename)
print("Report Generated ...", end='', flush=True)
print()
print("Mail Started ...", end='\r', flush=True)
# list_of_files = glob.glob('/home/ashwin.m/Documents/VAPT/Report/*.pdf') # * means all if need specific format then *.csv
# latest_file = max(list_of_files, key=os.path.getctime)

# print(list("/home/ashwin.m/Documents/VAPT/report"))
files = [pdf_filename]
# print(files)

for file in files:
    with open(file, 'rb') as f:
        file_data = f.read()
        file_name = f.name

# print(os.path.basename(file_name))
msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=os.path.basename(file_name))

with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.starttls()
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    smtp.send_message(msg)
print("Mail Sent ...", end='', flush=True)