#!/usr/local/bin/python3

## https://jira.readthedocs.io/en/latest/
## pip3 install jira

##https://pygithub.readthedocs.io/en/latest/reference.html
## pip3 install PyGithub

from jira import JIRA
from github import Github
from datetime import datetime
import sys

import json

def hours_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%dT%H:%M:%S.%f%z")
    d2 = datetime.strptime(d2, "%Y-%m-%dT%H:%M:%S.%f%z")
    return abs((d2 - d1).seconds//3600)

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

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

def getPRInfo(issues):
    g = Github(settings["github_api"])

    loops = len(issues) // 5
    print(len(issues), loops, sep=" ")

    try:
        for i in range(0,loops):
            min = i * 5
            if i == loops:
                max = ""
            else:
                max = (i+1) * 5
            q = "org:sonatype " + " OR ".join(issues[min:max])
            #print(q, min, max, sep=" ")
            ghIssues = g.search_issues(query=q)
            for ghIssue in ghIssues:
                if ghIssue.pull_request:
                    pr = ghIssue.as_pull_request()
                    print(ghIssue.pull_request.html_url, ghIssue.title, ghIssue.user.login, pr.comments, pr.additions, pr.changed_files, sep=", ", end=", ")
                    reviews = pr.get_reviews()
                    approved = []
                    approver_count = 0
                    commented = []
                    c_count = 0
                    for review in reviews:
                        #print(review.user.login, review.state, sep="|", end=", ")
                        if review.state == "APPROVED":
                            approved.append(review.user.login)
                            approver_count+=1
                        elif review.state == "COMMENTED":
                            commented.append(review.user.login)
                            c_count += 1
                    print(approver_count, end=",")
                    print(*approved, sep="|", end=",")
                    print(*commented, sep="|", end="")
                    print()
    except Exception as e:
        eprint(e)
        rate_limits = g.get_rate_limit()
        eprint(rate_limits.core, rate_limits.search, sep=", ")

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
    getPRInfo(issueKeys)


### run program
with open('settings.json') as f:
    settings = json.load(f)
    
main()
    