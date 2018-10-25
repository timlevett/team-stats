#!/usr/local/bin/python3

from jira import JIRA
from util import get_settings
from jira_sql_dao import insert_into_issue_duration_in_status
from jira_utils import get_statuses_and_time_spent_in
import sys
import datetime

settings = get_settings()
options = { 'server': settings["jira"]["server"] }
jira = JIRA(options, basic_auth=(settings["jira"]["user"], settings["jira"]["password"]))

def get_counts_for_period(period, team):
    JQL = f"project = CLM AND fixVersion = '{period}' AND Team = {team}"
    issues = jira.search_issues(JQL, maxResults=500)
    print(period, team, issues.total, issues.maxResults, sep=", ")

    for issue in issues:
        iType = issue.fields.issuetype.name
        if iType == 'Bug' and 'Nexus IQ:' in issue.fields.summary:
            iType = 'Policy'

        insert_into_issue_duration_in_status(period, team, issue.key, iType, get_statuses_and_time_spent_in(jira, issue))

planningPeriods = settings['planningPeriods']

for team in [17, 18, 35, 36, 38]:
    for period in planningPeriods:
        get_counts_for_period(period, team)
#get_counts_for_period('Joy', 35)

    