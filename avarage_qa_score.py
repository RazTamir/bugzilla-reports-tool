#!/usr/bin/env python
import google_api as gapi
from helpers import *
from datetime import datetime

REGRESSION = 15
BLOCKER = 30
TEST_BLOCKER = 20


now = datetime.today()
g = gapi.GoogleSpreadSheetAPI(
    f'{PRODUCT} QE - Quality Dashboard', "average_quality_score_data"
)


all_bugs = get_overall_backlog()
all_qa_scores = [get_quality_score(b) for b in all_bugs]
all_qa_scores = list(filter(lambda a: a != -1, all_qa_scores))
avarage_qa_score = sum(all_qa_scores) / len(all_qa_scores)
from ipdb import set_trace;set_trace()
g.insert_row(
    [now.strftime("%Y-%m-%d"), avarage_qa_score]
)



