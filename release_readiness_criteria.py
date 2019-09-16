#!/usr/bin/env python
import google_api as gapi
from helpers import *
import datetime

now = datetime.datetime.now()
g = gapi.GoogleSpreadSheetAPI('OCS QE - Quality Dashboard', 1)


g.update_sheet(1, 1, "Last update: {}".format(now.strftime("%Y-%m-%d %H:%M")))

qe_backlog = len(get_qe_backlog())
g.update_sheet(6, 3, qe_backlog)

dev_backlog = len(get_dev_backlog('ocs-4.2'))
g.update_sheet(6, 4, dev_backlog)

blockers = len(get_open_blockers())
g.update_sheet(6, 5, blockers)

candidate_blockers = len(get_open_candidate_blockers())
g.update_sheet(6, 6, candidate_blockers)

critical_bugs = len(get_critical_bugs())
g.update_sheet(6, 7, critical_bugs)

regressions = len(get_regression_bugs())
g.update_sheet(6, 8, regressions)

untriaged = len(get_untriaged_bugs())
g.update_sheet(6, 9, untriaged)

dec_bugs = len(get_doc_bugs())
g.update_sheet(6, 10, dec_bugs)

overall_backlog = len(get_overall_backlog())
g.update_sheet(6, 11, overall_backlog)

top_10_bugs = sort_by_pm_score(get_dev_backlog('ocs-4.2'))[:10]
for idx, bug in enumerate(top_10_bugs):
    row = 10 + idx
    column = 7
    g.update_sheet(
        row,
        column,
        '=HYPERLINK("https://bugzilla.redhat.com/show_bug.cgi?id={}", "{}")'.format(
            bug.bug_id, bug.bug_id
        )
    )
    g.update_sheet(row, column+1, bug.summary)
    g.update_sheet(row, column+6, bug.status)
    g.update_sheet(row, column+7, bug.component)
    g.update_sheet(row, column+8, bug.severity)

# Regression rate
all_bugs = len(get_all_bugs())
all_regressions = len(get_all_regression_bugs())
regression_rate = round((all_regressions / float(all_bugs)), 4)
g.update_sheet(10, 2, regression_rate)

# FailedQA rate
all_failed_qa = len(get_all_failedqa_bugs())
failed_qa_rate = round((all_failed_qa / float(all_bugs)), 4)
g.update_sheet(13, 2, failed_qa_rate)
