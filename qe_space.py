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
    bug_to_member[qa_contact].append(bug)

row = 4
col = 2
for key, bugs in bug_to_member.items():
    bugs_distribution = dict()
    bugs_distribution['urgent'] = filter_by_severity(bugs, 'urgent')
    bugs_distribution['high'] = filter_by_severity(bugs, 'high')
    bugs_distribution['medium'] = filter_by_severity(bugs, 'medium')
    bugs_distribution['low'] = filter_by_severity(bugs, 'low')
    idx = col
    g.update_sheet(row, col, key)
    for key, val in bugs_distribution.items():
        idx += 1
        if len(val) > 0:
            bug_ids = [str(bug.id) for bug in val]
            link = get_bug_url_link(bug_ids)
            g.update_sheet(row, idx, f'=HYPERLINK("{str(link)}", "{len(val)}")')
        else:
            if not g.get_cell_value(row, idx) == '-':
                g.update_sheet(row, idx, '-')
    row += 1
for row in range(row, 30 + 1):
    if g.get_cell_value(row, col):
        g.update_sheet(row, col, "")
        g.update_sheet(row, col + 1, "")
        g.update_sheet(row, col + 2, "")
        g.update_sheet(row, col + 3, "")
        g.update_sheet(row, col + 4, "")
    else:
        break

g.update_sheet(1, 1, f'Last update: {now.strftime("%Y-%m-%d %H:%M")}')