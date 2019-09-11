import bugzilla
from personal_config import *

# [CHANGE NEEDED] Add the relevant information for you report
PRODUCT = 'OCS'
VERSION42 = "4.2"

# [CHANGE NEEDED] List here all you teams you want to sample, for example:
manage = "manage"
e2e = "e2e"
ecosystem = "ecosystem"

all_team = [manage, e2e, ecosystem]

severity = {
    "urgent": 1,
    "high": 2,
    "medium": 3,
    "low": 4,
    "unspecified": 5
}

# [CHANGE NEEDED] modify the team names
BUGS_BY_TEAM = {
    manage: [],
    e2e: [],
    ecosystem: [],
}

# [CHANGE NEEDED] Add the team members divided into teams. For example:
teams = {
    manage: [
        "ebenahar", "belimele", "ebondare", "hnallurv", "jijoy", "nberry",
        "pbyregow", "prsurve", "sshreeka", "sagrawal", "tdesala",
        "fbalak", "mbukatov"
    ],
    e2e: [
        "tmuthami", "kramdoss", "akrai", "ksandha", "rperiyas", "sraghave",
        "tunguyen", "wusui", "yweinste"
    ],
    ecosystem: [
        "pbalogh", "clacroix", "dahorak", "shmohan", "vavuthu",
        "ratamir", "vakulkar"
    ],
}

# [CHANGE NEEDED] Add *ALL* the product components exist in Bugzilla
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
    'ocs-operator': []

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
