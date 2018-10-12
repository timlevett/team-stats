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
                    if startDate is not None:
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
    
