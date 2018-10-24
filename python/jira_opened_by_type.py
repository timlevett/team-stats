#!/usr/local/bin/python3

from jira import JIRA
from util import get_settings
import sys

settings = get_settings()
options = { 'server': settings["jira"]["server"] }
jira = JIRA(options, basic_auth=(settings["jira"]["user"], settings["jira"]["password"]))
JQL = "project = CLM AND createdDate >= '[BEG]' AND createdDate <= '[END]'"

def get_counts_for_period(period, beg, end):
    print()
    print(period, beg, end, sep=", ")
    issues = jira.search_issues(JQL.replace('[BEG]',beg).replace('[END]',end), maxResults=500)
    print(issues.total, issues.maxResults, issues.isLast, sep=", ")

    counts = {}

    for issue in issues:
        iType = issue.fields.issuetype.name
        if iType == 'Bug' and 'Nexus IQ:' in issue.fields.summary:
            iType = 'Policy'
        if iType in counts:
            counts[iType] = counts[iType] + 1
        else:
            counts[iType] = 1
    print(counts)

planningPeriods = settings['planningPeriods']

for period in planningPeriods:
    get_counts_for_period(period, planningPeriods[period][0:10],planningPeriods[period][12:])