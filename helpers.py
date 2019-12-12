from __future__ import division, print_function
import sys
import copy
import smtplib
import ssl
from config import *

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

BASE_QUERY = {
    "bug_status": None,
    "f3" : "OP",
    "f4" : "product",
    "f6" : "CP",
    "f8" : "flagtypes.name",
    "j3" : "OR",
    "o4" : "equals",
    "o8" : "anywordssubstr",
    "query_format" : "advanced",
    "v4" : BUGZILLA_PRODUCT,
    "v8" : ""
}


def send_email(gmail_user, gmail_password, recipients, subject, body):

    sent_from = gmail_user

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = gmail_user
    msg['To'] = ", ".join(recipients)

    # Create the body of the message (a plain-text and an HTML version).
    text = body

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, recipients, msg.as_string())
        server.close()

        print('Email sent!')
    except:
        print('Something went wrong...{}', sys.exc_info()[0])


def all_members():
    memb_list = teams.values()
    return [mem for team in memb_list for mem in team]


def all_bugs(bugs_dict):
    bug_list = bugs_dict.values()
    return [bug for comp in bug_list for bug in comp]


def get_bug_url_link(bug_ids):
    return (
        "https://bugzilla.redhat.com/buglist.cgi?bug_id={}".format(
            ','.join(bug_ids)
        )
    )


def report_needinfos():
    team_bugs = []
    needinfos = get_needinfos_bugs()
    all_team_members = all_members()

    for bug in needinfos:
        bug_flags = bug.flags[0]
        requestee = bug_flags.get('requestee')
        try:
            req = requestee.split("@")[0]
            if req in all_team_members:
                team_bugs.append(bug)
        except AttributeError as ex:
            print(
                "No needinfo contact for bug {}".format(bug.id)
            )

    for bug in team_bugs:
        short_url = get_bug_url_link([str(bug.id)])
        link = "<a href='{}' target='_blank'>(Link)".format(short_url)
        print(
            "<li>{} [{}] [{}]: {}  {}</li>".format(
                bug.bug_id, bug.status, bug.flags[0].get('requestee').split("@")[0], bug.summary, link
            )
        )


def report_status_on_qa():
    on_qa = get_on_qa_bugs()
    total_on_qa = len(on_qa)
    bug_id_list = [str(bug.id) for bug in on_qa]
    short_url = get_bug_url_link(bug_id_list)
    link = ""
    if len(bug_id_list):
        link = "<a href='{}' target='_blank'>(Link)".format(short_url)
    print(
        "<h3>Total ON_QA: {} {}</h3>".format(total_on_qa, link)
    )


def report_new_arrivals():
    new_bugs = get_new_arrivals()
    new_bugs = filter_by_component(new_bugs)
    total_new = len(all_bugs(new_bugs))
    print(
        "<h3>New arrivals (weekly): {}</h3>".format(total_new)
    )
    for comp, bugs in new_bugs.items():
        bug_id_list = []
        bugs.sort(key=lambda x: severity[x.bug_severity])
        if bugs:
            print(
                "<u><b><ul style='padding-left:10px;'>Component {} bugs:"
                "</ul></b></u>".format(comp, len(bugs))
            )
        for new_bug in bugs:
            print("<li>Bug {} [{}] [{}]: {}</li>".format(
                new_bug.bug_id, new_bug.bug_severity, new_bug.status,
                new_bug.short_desc
            ))
            bug_id_list.append(str(new_bug.bug_id))
        if len(bug_id_list) > 0:
            bug_link = get_bug_url_link(bug_ids=bug_id_list)
            link = "<a href='{}' target='_blank'>here".format(bug_link)
            print("<p>&nbsp;&nbsp;&nbsp;Link to bugs: {}</p>".format(link))


def report_resolved_bugs():
    resolved_bugs = get_resolved_bugs()
    resolved_bugs = filter_by_component(resolved_bugs)
    total_new = len(all_bugs(resolved_bugs))
    print(
        "<h3>Resolved bugs (weekly): {}</h3>".format(total_new)
    )


def report_open_blockers():
    open_blockers = get_open_blockers()
    open_blockers = filter_by_status(open_blockers, OPEN_BUGS)
    open_blockers = filter_by_component(open_blockers)
    total_blockers = len(all_bugs(open_blockers))
    print(
        "<h3>Open Blocker+: {}</h3>".format(total_blockers)
    )
    for comp, bugs in open_blockers.items():
        bug_id_list = []
        bugs.sort(key=lambda x: severity[x.bug_severity])
        if bugs:
            print(
                "<u><b><ul style='padding-left:10px;'>Component {} bugs:"
                "</ul></b></u>".format(comp, len(bugs))
            )
        for blocker in bugs:
            print("<li>Bug {} [{}] [{}]: {}</li>".format(
                blocker.bug_id, blocker.bug_severity, blocker.status,
                blocker.short_desc
            ))
            bug_id_list.append(str(blocker.bug_id))
        if len(bug_id_list) > 0:
            bug_link = get_bug_url_link(bug_ids=bug_id_list)
            link = "<a href='{}' target='_blank'>here".format(bug_link)
            print("<p>&nbsp;&nbsp;&nbsp;Link to bugs: {}</p>".format(link))


def report_open_candidate_blockers():
    open_blockers = get_open_candidate_blockers()
    open_blockers = filter_by_status(open_blockers, OPEN_BUGS)
    open_blockers = filter_by_component(open_blockers)
    total_blockers = len(all_bugs(open_blockers))
    print(
        "<h3>Open Blocker?: {}</h3>".format(total_blockers)
    )
    for comp, bugs in open_blockers.items():
        bug_id_list = []
        bugs.sort(key=lambda x: severity[x.bug_severity])
        if bugs:
            print("<u><b><ul style='padding-left:10px;'>Component {} bugs:"
                "</ul></b></u>".format(comp, len(bugs))
            )
        for blocker in bugs:
            print("<li>Bug {} [{}] [{}]: {}</li>".format(
                blocker.bug_id, blocker.bug_severity, blocker.status,
                blocker.short_desc
            ))
            bug_id_list.append(str(blocker.bug_id))
        if len(bug_id_list) > 0:
            bug_link = get_bug_url_link(bug_ids=bug_id_list)
            link = "<a href='{}' target='_blank'>here".format(bug_link)
            print("<p>&nbsp;&nbsp;&nbsp;Link to bugs: {}</p>".format(link))


def filter_by_component(bugs):
    bugs_by_comp = copy.deepcopy(COMPONENTS)
    for bug in bugs:
        if not (
            bug.status in OPEN_BUGS or bug.status in (
                VERIFIED or bug.status in ON_QA
            )
        ):
            continue
        if bug.component in bugs_by_comp:
            bugs_by_comp[bug.component].append(bug)
        else:
            continue
    return bugs_by_comp


def filter_by_team(bugs):
    bugs_by_team = copy.deepcopy(BUGS_BY_TEAM)
    for bug in bugs:
        if not (
            bug.status in OPEN_BUGS or bug.status in (
                VERIFIED or bug.status in ON_QA
            )
        ):
            continue
        try:
            qa_contact = bug.qa_contact_detail['email'].split('@')[0]
            if qa_contact in all_members():
                for team, members in teams.items():
                    if qa_contact in members:
                        bugs_by_team[team].append(bug)
        except AttributeError as ex:
            print("No needinfo contact for bug {}".format(bug.id))

    return bugs_by_team


def filter_by_status(bugs, status):
    return [bug for bug in bugs if bug.status in status]


def filter_by_severity(bugs, severity):
    return [bug for bug in bugs if bug.bug_severity in severity]


def report_on_qa_blockers():

    def print_report(bugs):
        bug_list = []
        bugs.sort(key=lambda x: severity[x.bug_severity])
        print("<ul style='list-style-type:circle'>")
        for bug in bugs:
            print(
                "<li>Bug {} [{}]: {}</li>".format(
                    bug.bug_id, bug.bug_severity, bug.short_desc
                )
            )
            bug_list.append(str(bug.id))
        print("</ul>")
        if len(bug_list) > 0:
            short_url = get_bug_url_link(bug_list)
            link = "<a href='{}' target='_blank'>here".format(short_url)
            print(
                "<p>&emsp;&emsp;&emsp;Link to bugs: {}</p>".format(link)
            )

    on_qa_blockers = get_on_qa_blockers()
    total_on_qa_blockers = len(on_qa_blockers)
    bug_id_list = [str(bug.id) for bug in on_qa_blockers]
    short_url = get_bug_url_link(bug_id_list)
    link = ""
    if len(bug_id_list) > 0:
        link = "<a href='{}' target='_blank'>(Link)".format(short_url)
    print(
        "<h3>ON_QA Blocker+: {} {}</h3>".format(total_on_qa_blockers, link)
    )
    print_report(on_qa_blockers)


def get_needinfos_bugs():
    all_team_members = all_members()
    all_team_members = ",".join(all_team_members)
    query = {
        "bug_status" : "",
        "classification" : "Red Hat",
        "f1" : "requestees.login_name",
        "f2" : "flagtypes.name",
        "include_fields" : [
            "id",
            "keywords",
            "flags",
            "summary",
            "flags_all",
            "qa_contact",
            "qa_contact_realname",
            "short_desc",
            "short_short_desc",
            "status",
            "whiteboard",
            "changeddate",
            "severity",
            "target_milestone"
        ],
        "o1" : "anywordssubstr",
        "o2" : "substring",
        "product" : BUGZILLA_PRODUCT,
        "query_format" : "advanced",
        "v1" : all_team_members,
        "v2" : "needinfo"
    }
    bugs = bzapi.query(query)
    return filter_only_bugs(bugs)


def sort_target_release(bugs):
    target_release = {}
    for bug in bugs:
        if bug.target_milestone in target_release:
            target_release[bug.target_milestone].append(bug)
        else:
            target_release[bug.target_milestone] = [bug]
    return target_release


def sort_by_pm_score(bugs):
    return sorted(bugs, key=lambda x: int(x.cf_pm_score), reverse=True)


def filter_only_bugs(bug_list):
    filtered_list = []
    for bug in bug_list:
        if "FutureFeature" in bug.keywords or "Improvement" in bug.keywords:
            continue
        else:
            filtered_list.append(bug)
    return filtered_list


def get_new_arrivals(changed_from='-1w', changed_to="Now"):
    query = {
        "action" : "wrap",
        "chfield" : "[Bug creation]",
        "chfieldfrom" : changed_from,
        "chfieldto" : changed_to,
        "f3" : "OP",
        "f4" : "product",
        "f6" : "CP",
        "j3" : "OR",
        "o4" : "equals",
        "query_format" : "advanced",
        "target_milestone" : "---",
        "v4" : BUGZILLA_PRODUCT
    }
    bugs = bzapi.query(query)
    return filter_only_bugs(bugs)


def get_blocker_arrivals(changed_from='-1w', changed_to="Now"):
    query = {
       "bug_status" : "",
       "chfield" : "[Bug creation]",
       "chfieldfrom" : changed_from,
       "chfieldto" : changed_to,
       "f3" : "OP",
       "f4" : "product",
       "f6" : "CP",
       "f7" : "flagtypes.name",
       "j3" : "OR",
       "o4" : "equals",
       "o7" : "substring",
       "query_format" : "advanced",
       "v4" : BUGZILLA_PRODUCT,
       "v7" : "blocker"
    }
    bugs = bzapi.query(query)
    return filter_only_bugs(bugs)


def get_resolved_bugs(changed_from='-1w', changed_to="Now"):
    query = {
        "bug_status": "",
        "chfield": "bug_status",
        "chfieldfrom": changed_from,
        "chfieldto": changed_to,
        "chfieldvalue": "ON_QA",
        "classification": "Red Hat",
        "f3": "OP",
        "f6": "CP",
        "j3": "OR",
        "product": BUGZILLA_PRODUCT,
        "query_format": "advanced"
    }
    bugs = bzapi.query(query)
    bugs = filter_by_status(bugs, [ON_QA, VERIFIED])
    return filter_only_bugs(bugs)


def get_qe_backlog():
    query = {
        "bug_status": "ON_QA",
        "f3": "OP",
        "f4": "product",
        "f6": "CP",
        "f7": "flagtypes.name",
        "j3": "OR",
        "o4": "equals",
        "o7": "substring",
        "query_format": "advanced",
        "v4": BUGZILLA_PRODUCT,
        "v7": BUGZILLA_VERSION_FLAG
    }
    bugs = bzapi.query(query)
    return bugs


def get_dev_backlog(version):
    query = {
        "bug_status": "NEW,ASSIGNED,POST,MODIFIED,ON_DEV",
        "f3": "OP",
        "f4": "product",
        "f6": "CP",
        "f7": "component",
        "f8": "flagtypes.name",
        "j3": "OR",
        "n7": "1",
        "o4": "equals",
        "o7": "equals",
        "o8": "substring",
        "query_format": "advanced",
        "v4": BUGZILLA_PRODUCT,
        "v7": "documentation",
        "v8": version

    }
    bugs = bzapi.query(query)
    bugs = filter_by_status(bugs, OPEN_BUGS_LIST)
    return bugs


def get_critical_bugs():
    bugs = []
    query = {
        "action": "wrap",
        "bug_severity": "urgent",
        "bug_status": "NEW,ASSIGNED,POST,MODIFIED",
        "f3": "OP",
        "f4": "product",
        "f6": "CP",
        "j3": "OR",
        "keywords": "FutureFeature, Improvement, ",
        "keywords_type": "nowords",
        "o4": "equals",
        "query_format": "advanced",
        "v4": BUGZILLA_PRODUCT

    }
    urgent_bugs = bzapi.query(query)
    bugs += filter_by_status(urgent_bugs, OPEN_BUGS_LIST)
    return bugs


def get_regression_bugs():
    query = {
        "action": "wrap",
        "bug_status": "NEW,ASSIGNED,POST,MODIFIED",
        "f3": "OP",
        "f4": "product",
        "f6": "CP",
        "f7": "keywords",
        "j3": "OR",
        "o4": "equals",
        "o7": "anywordssubstr",
        "query_format": "advanced",
        "v4": BUGZILLA_PRODUCT,
        "v7": "Regression"

    }
    bugs = bzapi.query(query)
    bugs = filter_by_status(bugs, OPEN_BUGS_LIST)
    return bugs


def get_untriaged_bugs(version_flag):
    query = {
        "bug_status": "NEW,ASSIGNED,POST,MODIFIED,ON_DEV,ON_QA,VERIFIED,RELEASE_PENDING",
        "f3": "OP",
        "f4": "product",
        "f6": "CP",
        "f7": "flagtypes.name",
        "f8": "component",
        "j3": "OR",
        "n8": "1",
        "o4": "equals",
        "o7": "regexp",
        "o8": "substring",
        "query_format": "advanced",
        "v4": BUGZILLA_PRODUCT,
        "v7": f'{version_flag}.*[?]',
        "v8": "Documentation"


    }
    bugs = bzapi.query(query)
    bugs = filter_by_status(bugs, [
        "NEW", "ASSIGNED", "POST", "MODIFIED", "ON_DEV", "ON_QA",
        "VERIFIED", "RELEASE_PENDING"
    ])
    return bugs


def get_doc_bugs():
    query = {
        "bug_status": "NEW,ASSIGNED,POST,MODIFIED,ON_DEV",
        "f3": "OP",
        "f4": "product",
        "f6": "CP",
        "f7": "component",
        "f8": "flagtypes.name",
        "f9": "keywords",
        "j3": "OR",
        "o4": "equals",
        "o7": "equals",
        "o8": "substring",
        "o9": "notsubstring",
        "query_format": "advanced",
        "v4": BUGZILLA_PRODUCT,
        "v7": "documentation",
        "v8": BUGZILLA_VERSION_FLAG,
        "v9": "Tracking"
    }
    bugs = bzapi.query(query)
    bugs = filter_by_status(bugs, OPEN_BUGS_LIST)
    return bugs


def get_performance_blockers():
    query = {
        "bug_status": "NEW,ASSIGNED,POST,MODIFIED",
        "classification": "Red Hat",
        "f3": "OP",
        "f6": "CP",
        "j5": "OR",
        "keywords": "TestBlocker, Performance, ",
        "keywords_type": "allwords",
        "product": BUGZILLA_PRODUCT,
        "query_format": "advanced"
    }
    bugs = bzapi.query(query)
    bugs = filter_by_status(bugs, OPEN_BUGS_LIST)
    return bugs


def get_scale_blockers():
    query = {
        "bug_status": "NEW,ASSIGNED,POST,MODIFIED",
        "classification": "Red Hat",
        "f3": "OP",
        "f6": "CP",
        "f7": "cf_qa_whiteboard",
        "keywords": "TestBlocker,",
        "keywords_type": "allwords",
        "o7": "substring",
        "product": BUGZILLA_PRODUCT,
        "query_format": "advanced",
        "v7": "Scale"
    }
    bugs = bzapi.query(query)
    bugs = filter_by_status(bugs, OPEN_BUGS_LIST)
    return bugs


def get_overall_backlog(version=''):
    query = {
        "action": "wrap",
        "bug_status": "NEW,ASSIGNED,POST,MODIFIED,ON_DEV",
        "f3": "OP",
        "f4": "product",
        "f6": "CP",
        "j3": "OR",
        "o4": "equals",
        "query_format": "advanced",
        "v4": BUGZILLA_PRODUCT,
    }
    if version:
        query['f7'] = "flagtypes.name"
        query['o7'] = 'substring'
        query['v7'] = version
    bugs = bzapi.query(query)
    bugs = filter_by_status(bugs, OPEN_BUGS_LIST)
    return bugs


def get_all_bugs():
    query = {
        "action": "wrap",
        "bug_status": "__open__,__closed__",
        "f3": "OP",
        "f4": "product",
        "f6": "CP",
        "j3": "OR",
        "o4": "equals",
        "query_format": "advanced",
        "v4": BUGZILLA_PRODUCT

    }
    bugs = bzapi.query(query)
    return bugs


def get_all_regression_bugs():
    query = {
        "action": "wrap",
        "bug_status": "__open__,__closed__",
        "f3": "OP",
        "f4": "product",
        "f6": "CP",
        "f7": "keywords",
        "j3": "OR",
        "o4": "equals",
        "o7": "anywordssubstr",
        "query_format": "advanced",
        "v4": BUGZILLA_PRODUCT,
        "v7": "Regression"

    }
    bugs = bzapi.query(query)
    return bugs


def get_all_failedqa_bugs():
    query = {
        "action": "wrap",
        "bug_status": "__open__,__closed__",
        "f3": "OP",
        "f4": "product",
        "f6": "CP",
        "f7": "cf_verified",
        "j3": "OR",
        "o4": "equals",
        "o7": "substring",
        "query_format": "advanced",
        "v4": BUGZILLA_PRODUCT,
        "v7": "FailedQA"
    }
    bugs = bzapi.query(query)
    return bugs


def get_all_verified_bugs():
    query = {
        "bug_status": "VERIFIED,RELEASE_PENDING,CLOSED",
        "f3": "OP",
        "f4": "product",
        "f6": "CP",
        "f7": "bug_status",
        "j3": "OR",
        "o4": "equals",
        "o7": "changedto",
        "query_format": "advanced",
        "v4": BUGZILLA_PRODUCT,
        "v7": "VERIFIED"
    }
    bugs = bzapi.query(query)
    return bugs


def get_verified_bugs(changed_from='-1w', changed_to='Now'):
    query = {
        "bug_status": "",
        "chfield": "bug_status",
        "chfieldfrom": changed_from,
        "chfieldto": changed_to,
        "chfieldvalue": "VERIFIED",
        "classification": "Red Hat",
        "f3": "OP",
        "f6": "CP",
        "j3": "OR",
        "product": BUGZILLA_PRODUCT,
        "query_format": "advanced"
    }
    bugs = bzapi.query(query)
    return bugs


def get_changed_bugs_in_the_past_x_time(time='-1h'):
    query = {
        "bug_status": "NEW,ASSIGNED,POST,MODIFIED,ON_DEV,VERIFIED,ON_QA,RELEASE_PENDING",
        "classification": "Red Hat",
        "f3": "OP",
        "f6": "CP",
        "f9": "delta_ts",
        "j3": "OR",
        "o9": "greaterthan",
        "product": BUGZILLA_PRODUCT,
        "query_format": "advanced",
        "v9": time
    }

    bugs = bzapi.query(query)
    bugs = filter_by_status(bugs, [
        "NEW", "ASSIGNED", "POST", "MODIFIED", "ON_DEV", "VERIFIED", "ON_QA",
        "RELEASE_PENDING"
    ])
    return bugs


def get_quality_score(bug):
    qa_wb = bug.cf_qa_whiteboard
    if QUALITY_IMPACT in qa_wb:
        score_idx = int(qa_wb.find(QUALITY_IMPACT) + len(QUALITY_IMPACT))
        return int(qa_wb[score_idx:score_idx + 3])
    return -1


def get_all_ready_for_testing_bugs():
    query = {
        "bug_status": "",
        "f3": "OP",
        "f4": "product",
        "f6": "CP",
        "f7": "bug_status",
        "j3": "OR",
        "keywords": "Reopened",
        "keywords_type": "nowords",
        "o4": "equals",
        "o7": "changedto",
        "query_format": "advanced",
        "v4": BUGZILLA_PRODUCT,
        "v7": "ON_QA"
    }
    bugs = bzapi.query(query)
    return bugs


def get_on_qa_bugs():
    query = BASE_QUERY.copy()
    query['bug_status'] = ON_QA
    bugs = bzapi.query(query)
    return filter_only_bugs(bugs)


def get_open_blockers():
    query = {
        "action": "wrap",
        "bug_status": "NEW,ASSIGNED,POST,MODIFIED",
        "f3": "OP",
        "f4": "product",
        "f6": "CP",
        "f8": "flagtypes.name",
        "f9": "flagtypes.name",
        "j3": "OR",
        "o4": "equals",
        "o8": "anywordssubstr",
        "o9": "substring",
        "query_format": "advanced",
        "v4": BUGZILLA_PRODUCT,
        "v8": "blocker+",
        "v9": BUGZILLA_VERSION_FLAG
    }
    bugs = bzapi.query(query)
    bugs = filter_by_status(bugs, OPEN_BUGS_LIST)
    return bugs


def get_open_candidate_blockers():
    query = {
        "action": "wrap",
        "bug_status": "NEW,ASSIGNED,POST,MODIFIED",
        "f3": "OP",
        "f4": "product",
        "f6": "CP",
        "f8": "flagtypes.name",
        "f9": "flagtypes.name",
        "j3": "OR",
        "o4": "equals",
        "o8": "anywordssubstr",
        "o9": "substring",
        "query_format": "advanced",
        "v4": BUGZILLA_PRODUCT,
        "v8": "blocker?",
        "v9": BUGZILLA_VERSION_FLAG
    }
    bugs = bzapi.query(query)
    bugs = filter_by_status(bugs, OPEN_BUGS_LIST)
    return bugs


def get_on_qa_blockers():
    query = BASE_QUERY.copy()
    query['bug_status'] = ON_QA
    query['v8'] = BLOCKER
    bugs = bzapi.query(query)
    return filter_only_bugs(bugs)


def get_deployment_blockers():
    query = {
        "bug_status": "NEW,ASSIGNED,POST,MODIFIED",
        "f3": "OP",
        "f4": "product",
        "f6": "CP",
        "f7": "cf_qa_whiteboard",
        "j3": "OR",
        "o4": "equals",
        "o7": "anywordssubstr",
        "query_format": "advanced",
        "v4": BUGZILLA_PRODUCT,
        "v7": "Deployment_blocker"

    }
    bugs = bzapi.query(query)
    bugs = filter_by_status(bugs, OPEN_BUGS_LIST)
    return bugs


def get_feature_blockers():
    query = {
        "bug_status": "NEW,ASSIGNED,POST,MODIFIED",
        "f3": "OP",
        "f4": "product",
        "f6": "CP",
        "f7": "cf_qa_whiteboard",
        "j3": "OR",
        "o4": "equals",
        "o7": "anywordssubstr",
        "query_format": "advanced",
        "v4": BUGZILLA_PRODUCT,
        "v7": "Feature_blocker"

    }
    bugs = bzapi.query(query)
    bugs = filter_by_status(bugs, OPEN_BUGS_LIST)
    return bugs


def get_stability_bugs():
    query = {
        "bug_status": "NEW,ASSIGNED,POST,MODIFIED",
        "f3": "OP",
        "f4": "product",
        "f6": "CP",
        "f7": "cf_qa_whiteboard",
        "j3": "OR",
        "o4": "equals",
        "o7": "anywordssubstr",
        "query_format": "advanced",
        "v4": BUGZILLA_PRODUCT,
        "v7": "Stability"

    }
    bugs = bzapi.query(query)
    bugs = filter_by_status(bugs, OPEN_BUGS_LIST)
    return bugs
