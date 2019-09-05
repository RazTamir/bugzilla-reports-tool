#!/usr/bin/env python
import datetime

from helpers import *
from personal_config import *
import sys
from email.mime.text import MIMEText

VERSION42 = "4.2"

temp = sys.stdout
sys.stdout = open('report_{}_status'.format(PRODUCT), 'w')
print("<html><body>")
print("<h3>Hi,</h3>")
print("<h3>This is the status of {} - bugs:</h3>".format(PRODUCT))
print("<h1><u>{} {} Status</u></h1>".format(PRODUCT, VERSION42))
report_new_arrivals()
report_resolved_bugs()
report_status_on_qa(VERSION42)
report_on_qa_blockers(VERSION42)
report_open_blockers(VERSION42)
report_open_candidate_blockers(VERSION42)

print("<p></p>")
print("<h3>Thanks</h3>")
print("</body></html>")
sys.stdout = temp
raport_file = open('report_{}_status'.format(PRODUCT), 'rb')
report = MIMEText(raport_file.read())
raport_file.close()
now = datetime.datetime.now()
date = "%s %s %s" % (now.strftime("%b"), now.strftime("%d"), now.year)
send_email(
    gmail_user, gmail_pwd, [mail_to],
    "Bugzilla report [{}] - {} QE Status".format(date, PRODUCT),
    report.as_string()
)
