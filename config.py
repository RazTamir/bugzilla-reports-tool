import bugzilla
import yaml
import sys
import os
import google_api as gapi

# [CHANGE NEEDED] Add the relevant information for you report
cfg_path = os.path.expanduser('~/.gapi/personal_cfg.yml')

if len(sys.argv) != 2:
    raise IndexError("You must provide the spreadsheet name to work with")

SPREADSHEET_NAME = sys.argv[1]
with open(cfg_path, 'r') as ymlfile:
    cfg = yaml.full_load(ymlfile)
    USER = cfg['bugzilla']['user']
    PASSWORD = cfg['bugzilla']['password']

    # For the Bugzilla reports
    gmail_user = cfg['bugzilla_report']['gmail_address']
    gmail_pwd = cfg['bugzilla_report']['gmail_pass']
    mail_to = USER

g = gapi.GoogleSpreadSheetAPI(SPREADSHEET_NAME, "Dashboard configuration")

PRODUCT = g.get_cell_value(7, 3)
BUGZILLA_PRODUCT = g.get_cell_value(7, 4)
VERSION = g.get_cell_value(7, 6)
# The version flag should contain only x and y releases:
# ocs-4.2.0 --> ocs-x.y.z so you'll need to add only ocs-4.2 in order to see
# all bugs in version x.y
BUGZILLA_VERSION_FLAG = g.get_cell_value(7, 5)

# [CHANGE NEEDED] List here all the teams you want to sample, for example:
team1 = "manage"
team2 = "e2e"
team3 = "ecosystem"

all_team = [team1, team2, team3]

severity = {
    "urgent": 1,
    "high": 2,
    "medium": 3,
    "low": 4,
    "unspecified": 5
}

BUGS_BY_TEAM = {
    team1: [],
    team2: [],
    team3: [],
}

# [CHANGE NEEDED] Add the team members divided into teams. For example:
teams = {
    team1: [
        "ebenahar", "belimele", "ebondare", "hnallurv", "jijoy", "nberry",
        "pbyregow", "prsurve", "sshreeka", "sagrawal", "tdesala",
        "fbalak", "mbukatov", "apolak", "srozen",
    ],
    team2: [
        "tmuthami", "kramdoss", "akrai", "ksandha", "rperiyas", "sraghave",
        "tunguyen", "wusui", "alayani", "savetisy"
    ],
    team3: [
        "pbalogh", "clacroix", "dahorak", "shmohan", "vavuthu",
        "ratamir", "vakulkar"
    ],
}

# [CHANGE NEEDED] Add *ALL* the product components exist in Bugzilla for your
# product
COMPONENTS = {
    'ceph': [],
    'build': [],
    'csi-driver': [],
    'distribution': [],
    'documentation': [],
    'installation': [],
    'Multi-Cloud Object Gateway': [],
    'releng': [],
    'rook': [],
    'storage-dashboard': [],
    'unclassified': [],
    'ocs-operator': [],
    'must-gather': [],

}

backlog = {}
URL = "bugzilla.redhat.com"
bzapi = bugzilla.Bugzilla(URL, user=USER, password=PASSWORD)

# Bug statuses
VERIFIED = "VERIFIED"
ON_QA = "ON_QA"
MODIFIED = "MODIFIED"
OPEN_BUGS = "NEW,ASSIGNED,POST,MODIFIED"
OPEN_BUGS_LIST = ["NEW", "ASSIGNED", "POST", "MODIFIED"]

# Bug flags
BLOCKER = "blocker+"
CANDIDATE_BLOCKER = "blocker?"
MISSING_ACK = [
    "pm_ack+",
    "devel_ack+",
    "qa_ack?"
]
NEEDINFO = "needinfo?"
QUALITY_IMPACT = "quality_impact="
