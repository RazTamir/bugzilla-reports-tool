#!/usr/bin/env python
from helpers import *
from datetime import datetime

g = gapi.GoogleSpreadSheetAPI(SPREADSHEET_NAME, "GSS closed loop")
now = datetime.today()

open_gss = len(get_gss_closed_loop("qe_test_coverage?"))
acked_gss = len(get_gss_closed_loop("qe_test_coverage+"))
naked_gss = len(get_gss_closed_loop("qe_test_coverage-"))

g.insert_row([now.strftime("%Y-%m-%d"), open_gss, acked_gss, naked_gss])