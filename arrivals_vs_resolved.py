#!/usr/bin/env python
import google_api as gapi
from helpers import *
from datetime import datetime, timedelta

now = datetime.today() - timedelta(days=1)
g = gapi.GoogleSpreadSheetAPI(
    f'{PRODUCT} QE - Quality Dashboard', "arrivals_vs_resolved_data"
)

new_bugs = get_new_arrivals(
    changed_from=now.strftime("%Y-%m-%d"), changed_to=now.strftime("%Y-%m-%d")
)
resolved_bugs = get_resolved_bugs(
    changed_from=now.strftime("%Y-%m-%d"), changed_to=now.strftime("%Y-%m-%d")
)
verified_bugs = get_verified_bugs(
    changed_from=now.strftime("%Y-%m-%d"), changed_to=now.strftime("%Y-%m-%d")
)

g.insert_row(
    [now.strftime("%Y-%m-%d"), len(new_bugs), len(resolved_bugs),
     len(verified_bugs)]
)

