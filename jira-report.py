#!/usr/local/bin/python3

## https://jira.readthedocs.io/en/latest/
## pip3 install jira

##https://pygithub.readthedocs.io/en/latest/reference.html
## pip3 install PyGithub

from jira import JIRA
from util import hours_between, get_settings
from github_report import get_pull_request_information

import json


def getTimeSpentIn(jira, issue, statusToCheck):
    issueExplanded = jira.issue(issue.key, expand='changelog')
    changelog = issueExplanded.changelog
    startDate = None
    endDate = None
    for history in changelog.histories:
        for item in history.items:
            if item.field == 'status':
                if item.toString == statusToCheck:
                    startDate = history.created
                elif item.fromString == statusToCheck:
                    endDate = history.created
                #print('Date:' + history.created + ' From:' + item.fromString + ' To:' + item.toString)
    if startDate is None or endDate is None:
        return 0
    else:
        return hours_between(startDate, endDate)



def main():
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

    print()
    print('---pr info---')
    print("pull request url, summary, created_by, num of comments, num of additions, files_changed, approve count, approvers, commenters")
    get_pull_request_information(settings, issueKeys)

settings = get_settings()
    
main()
    
