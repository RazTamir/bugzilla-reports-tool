#!/usr/bin/env python
import google_api as gapi
from helpers import *
import datetime

now = datetime.datetime.now()
g = gapi.GoogleSpreadSheetAPI(
    f'{PRODUCT} QE - Quality Dashboard', "arrivals_vs_resolved_data"
)

new_bugs = get_new_arrivals(time_frame='-1d')
resolved_bugs = get_resolved_bugs(time_frame='-1d')

g.insert_row(
    [now.strftime("%m/%d/%y"), len(new_bugs), len(resolved_bugs)]
)

