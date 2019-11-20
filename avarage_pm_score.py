#!/usr/bin/env python
import google_api as gapi
from helpers import *
from datetime import datetime

now = datetime.today()
g = gapi.GoogleSpreadSheetAPI(
    f'{PRODUCT} QE - Quality Dashboard', "average_pm_score_data"
)

all_bugs = get_overall_backlog()
all_pm_scores = [int(b.cf_pm_score) for b in all_bugs]
avarage_pm_score = sum(all_pm_scores) / len(all_pm_scores)

g.insert_row(
    [now.strftime("%Y-%m-%d"), avarage_pm_score]
)

