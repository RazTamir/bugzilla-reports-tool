#!/usr/bin/env python
import datetime
import google_api as gapi

from reporttools.helpers import *


now = datetime.datetime.now()
g = gapi.GoogleSpreadSheetAPI(
    f'{PRODUCT} QE - Quality Dashboard', "Release Readiness Criteria"
)

g.update_sheet(1, 1, f'Last update: {now.strftime("%Y-%m-%d %H:%M")}')

qe_backlog = len(get_qe_backlog())
g.update_sheet(6, 3, qe_backlog)

dev_backlog = len(get_dev_backlog(BUGZILLA_VERSION_FLAG))
g.update_sheet(6, 4, dev_backlog)

blockers = len(get_open_blockers())
g.update_sheet(6, 5, blockers)

candidate_blockers = len(get_open_candidate_blockers())
g.update_sheet(6, 6, candidate_blockers)

critical_bugs = len(get_critical_bugs())
g.update_sheet(6, 7, critical_bugs)

regressions = len(get_regression_bugs())
g.update_sheet(6, 8, regressions)

untriaged = len(get_untriaged_bugs(BUGZILLA_VERSION_FLAG))
g.update_sheet(6, 9, untriaged)

dec_bugs = len(get_doc_bugs())
g.update_sheet(6, 10, dec_bugs)

overall_backlog = len(get_overall_backlog())
g.update_sheet(6, 11, overall_backlog)

top_10_bugs = sort_by_pm_score(get_dev_backlog(BUGZILLA_VERSION_FLAG))[:10]
for idx, bug in enumerate(top_10_bugs):
    row = 10 + idx
    column = 7
    g.update_sheet(
        row,
        column,
        (
            f'=HYPERLINK("https://bugzilla.redhat.com/show_bug'
            f'.cgi?id={bug.bug_id}", "{bug.bug_id}")'
        )
    )
    g.update_sheet(row, column+1, bug.summary)
    g.update_sheet(row, column+6, bug.status)
    g.update_sheet(row, column+7, bug.component)
    g.update_sheet(row, column+8, bug.severity)
    converted = datetime.datetime.strptime(
        bug.creation_time.value, "%Y%m%dT%H:%M:%S"
    )
    g.update_sheet(row, column + 9, (now - converted).days)


# Regression rate
all_bugs = len(get_all_bugs())
all_regressions = len(get_all_regression_bugs())
regression_rate = round((all_regressions / float(all_bugs)), 4)
g.update_sheet(10, 2, regression_rate)

# FailedQA rate
all_failed_qa = len(get_all_failedqa_bugs())
failed_qa_rate = round((all_failed_qa / float(all_bugs)), 4)
g.update_sheet(13, 2, failed_qa_rate)

# Verification rate
all_verified = len(get_all_verified_bugs())
all_ready_for_testing = len(get_all_ready_for_testing_bugs())
failed_qa_rate = round((all_verified / float(all_ready_for_testing)), 4)
g.update_sheet(16, 2, failed_qa_rate)

# Verification rate weekly
verified_weekly = 0
for c_from, c_to in [
    ('-1w', 'Now'), ('-2w', '-1w'), ('-3w', '-2w'), ('-4w', '-3w'),
    ('-5w', '-4w'), ('-6w', '-5w'), ('-7w', '-6w'), ('-8w', '-7w')
]:
    this_week = len(get_verified_weekly(c_from, c_to))
    verified_weekly += this_week
g.update_sheet(19, 2, verified_weekly / 8)
