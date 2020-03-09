#!/usr/bin/env python
from helpers import *
from datetime import datetime

now = datetime.today()
g = gapi.GoogleSpreadSheetAPI(SPREADSHEET_NAME, "QE Space")

qe_backlog = get_qe_backlog()
bug_to_member = dict()
for bug in qe_backlog:
    qa_contact = bug.qa_contact.split('@')[0]
    if qa_contact not in bug_to_member.keys():
        bug_to_member[qa_contact] = list()
    bug_to_member[qa_contact].append(str(bug.id))

row = 3
col = 2
for key, val in bug_to_member.items():
    link = get_bug_url_link(val)
    g.update_sheet(row, col, key)
    g.update_sheet(row, col+1, f'=HYPERLINK("{str(link)}", "{len(val)}")')
    row += 1
for row in range(row, 30 + 1):
    if g.get_cell_value(row, col):
        g.update_sheet(row, col, "")
        g.update_sheet(row, col + 1, "")
