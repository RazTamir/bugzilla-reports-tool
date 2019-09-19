import bugzilla
from personal_config import *

# [CHANGE NEEDED] Add the relevant information for you report
PRODUCT = 'OCS'
VERSION = "4.2"
BUGZILLA_PRODUCT = 'Red Hat OpenShift Container Storage'
BUGZILLA_VERSION_FLAG = 'ocs-4.2.0?'

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

VERSION_4_2 = ["---"]
VERSION_4_3 = ["---"]

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
