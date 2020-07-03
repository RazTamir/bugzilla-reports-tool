import time
import google_api as gapi
from helpers import *
import datetime

now = datetime.datetime.now()
g = gapi.GoogleSpreadSheetAPI(SPREADSHEET_NAME, "Layered products bugs")

qe_backlog = len(get_qe_backlog_by_component(
    product=LAYERED_PRODUCT, target_version=LAYERED_PRODUCT_VERSION, 
    component=LAYERED_PRODUCT_COMPONENT)
    )
g.update_sheet(6, 3, qe_backlog)

dev_backlog = len(get_dev_backlog_by_component(
    product=LAYERED_PRODUCT, target_version=LAYERED_PRODUCT_VERSION, 
    component=LAYERED_PRODUCT_COMPONENT)
    )
g.update_sheet(6, 4, dev_backlog)

overall_backlog = len(get_overall_backlog_by_component(
    product=LAYERED_PRODUCT, 
    component=LAYERED_PRODUCT_COMPONENT)
    )
g.update_sheet(6, 5, overall_backlog)
time.sleep(30)

all_affecting_product_urgent = len(get_dependent_product_bugs(BUGZILLA_PRODUCT, "urgent"))
g.update_sheet(6, 6, all_affecting_product_urgent)

all_affecting_product = len(get_dependent_product_bugs(BUGZILLA_PRODUCT))
g.update_sheet(6, 7, all_affecting_product)
