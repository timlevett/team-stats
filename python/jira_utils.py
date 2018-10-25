from jira import JIRA
from util import hours_between
import statistics


def get_numbers_for_time_spend_for_status(jira, issues, statusToCheck):
    sum = 0
    max = 0
    min = 0
    count = 0
    avg = 0
    issueHoursInStatus = []

    for issue in issues:
        time = getTimeSpentIn(jira, issue, statusToCheck)
        sum += time
        if max < time:
            max = time
        if min > time:
            min = time
        count += 1
        issueHoursInStatus.append(time)

    if count > 0:
        avg = sum // count
        stdDev = statistics.stdev(issueHoursInStatus)
        median = statistics.median(issueHoursInStatus)
    else:
        avg = 0
        stdDev = 0
        median = 0

    return count, sum, max, min, avg, stdDev, median

def getTimeSpentIn(jira, issue, statusToCheck):
    issueExplanded = jira.issue(issue.key, expand='changelog')
    changelog = issueExplanded.changelog
    startDate = None
    endDate = None
    hours = 0
    for history in changelog.histories:
        for item in history.items:
            if item.field == 'status':
                if item.toString == statusToCheck:
                    if startDate is not None and endDate is not None:
                        hours += hours_between(startDate, endDate)
                        endDate = None
                    startDate = history.created
                elif item.fromString == statusToCheck:
                    endDate = history.created
                #print('Date:' + history.created + ' From:' + item.fromString + ' To:' + item.toString)
    # print(startDate, endDate, sep="\n")
    # print(hours + hours_between(startDate, endDate))
    # print(hours_between(startDate, endDate))
    if startDate is None or endDate is None:
        return hours
    else:
        return hours + hours_between(startDate, endDate)

def get_time_spend_in(jira, issue, statusToCheck):
    issueExplanded = jira.issue(issue.key, expand='changelog')
    changelog = issueExplanded.changelog
    startDate = None
    endDate = None
    hours = 0
    count = 0
    for history in changelog.histories:
        for item in history.items:
            if item.field == 'status':
                if item.toString == statusToCheck:
                    if startDate is not None and endDate is not None:
                        hours += hours_between(startDate, endDate)
                        endDate = None
                        count += 1
                    startDate = history.created
                elif item.fromString == statusToCheck:
                    endDate = history.created
    if startDate is None or endDate is None:
        return startDate, endDate, count, hours
    else:
        return startDate, endDate, hours + hours_between(startDate, endDate)

def get_statuses_and_time_spent_in(jira, issue):
    issueExpanded = jira.issue(issue.key, expand='changelog')
    changelog = issueExpanded.changelog
    statuses = []
    current_status = None
    start_date = None
    for history in changelog.histories:
        for item in history.items:
            if item.field == 'status':
                if current_status is not None:
                    # log status change
                    statusHash = {}
                    statusHash['name'] = current_status
                    statusHash['start'] = start_date
                    statusHash['end'] = history.created
                    statusHash['duration_hours'] = hours_between(start_date, history.created)
                    statuses.append(statusHash)
                
                current_status = item.toString
                start_date = history.created
                
    return statuses


def get_transition_counts_for_issues(jira, issues):
    transitions = {}
    for issue in issues:
        curT = get_transition_counts(jira, issue)
        for key, value in curT.items():
            if key in transitions:
                transitions[key] = transitions[key] + value
            else:
                transitions[key] = value

    return transitions

def get_transition_counts(jira, issue):
    issueExplanded = jira.issue(issue.key, expand='changelog')
    changelog = issueExplanded.changelog

    transitions = {}

    for history in changelog.histories:
        for item in history.items:
            if item.field == 'status':
                if item.fromString is None:
                    frm = ""
                else:
                    frm = item.fromString
                key = ":".join([frm , item.toString])
                #print(key)
                if  key in transitions:
                    transitions[key] = transitions[key] + 1
                else:
                    transitions[key] = 1
                #print('Date:' + history.created + ' From:' + item.fromString + ' To:' + item.toString)
    
    return transitions




def print_jira_info(settings):
    options = { 'server': settings["jira"]["server"] }

    jira = JIRA(options, basic_auth=(settings["jira"]["user"], settings["jira"]["password"]))

    jql = settings["jql"]

    issues = jira.search_issues(jql)

    #print("There were " + str(len(issues)) + " issues returned from query `" + jql + "`")
    print ("key, summary, type, priority, resolution, reporter, assignee, time spent in review")
    issueKeys = []
    for issue in issues:
        print(issue.key, issue.fields.summary,issue.fields.issuetype.name, issue.fields.priority, issue.fields.resolution, issue.fields.reporter, issue.fields.assignee, getTimeSpentIn(jira, issue,'Waiting for Review'),sep=", ")
        issueKeys.append(issue.key)
    return issueKeys
    
