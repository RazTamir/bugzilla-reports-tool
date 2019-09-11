#!/usr/bin/env python
import google_api as gapi
from helpers import *
import datetime

now = datetime.datetime.now()
g = gapi.GoogleSpreadSheetAPI('OCS QE - Quality Dashboard', 1)


g.update_sheet(1, 1, "Last update: {}".format(now.strftime("%Y-%m-%d %H:%M")))

qe_backlog = len(get_qe_backlog('4.2'))
g.update_sheet(6, 3, qe_backlog)

dev_backlog = len(get_dev_backlog('4.2'))
g.update_sheet(6, 4, dev_backlog)

blockers = len(get_open_blockers('4.2'))
g.update_sheet(6, 5, blockers)

candidate_blockers = len(get_open_candidate_blockers('4.2'))
g.update_sheet(6, 6, candidate_blockers)

critical_bugs = len(get_critical_bugs('4.2'))
g.update_sheet(6, 7, critical_bugs)

regressions = len(get_regression_bugs('4.2'))
g.update_sheet(6, 8, regressions)

untriaged = len(get_untriaged_bugs('4.2'))
g.update_sheet(6, 9, untriaged)

dec_bugs = len(get_doc_bugs('4.2'))
g.update_sheet(6, 10, dec_bugs)

overall_backlog = len(get_overall_backlog('4.2'))
g.update_sheet(6, 11, overall_backlog)

all_bugs = len(get_all_bugs())
all_regressions = len(get_all_regression_bugs())
regression_rate = round((all_regressions / float(all_bugs)), 4)
g.update_sheet(13, 13, regression_rate)
