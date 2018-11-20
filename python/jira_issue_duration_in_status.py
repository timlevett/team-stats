#!/usr/local/bin/python3

from jira import JIRA
from util import get_settings
from jira_sql_dao import insert_into_issue_duration_in_status, delete_planning_period
from jira_utils import get_statuses_and_time_spent_in

settings = get_settings()
options = { 'server': settings["jira"]["server"] }
jira = JIRA(options, basic_auth=(settings["jira"]["user"], settings["jira"]["password"]))

def update_counts_for_period(period, team):
    JQL = f"project = CLM AND fixVersion = '{period}' AND Team = {team}"
    issues = jira.search_issues(JQL, maxResults=500)
    if issues.total == 500:
        print(f"WARNING: hit maxResults for {period} and {team}")


    delete_planning_period(period, team)
    for issue in issues:
        iType = issue.fields.issuetype.name
        if iType == 'Bug' and 'Nexus IQ:' in issue.fields.summary:
            iType = 'Policy'
        elif issue.fields.summary.startswith('Release IQ '):
            iType = 'Release'
        insert_into_issue_duration_in_status(period, team, issue.key, iType, get_statuses_and_time_spent_in(jira, issue))

planningPeriods = settings['planningPeriods']

for team in [17, 18, 35, 36, 38]:
    for period in planningPeriods:
        print(f"started planning period {period} and team {team}...")
        update_counts_for_period(period, team)
        print(f"completed planning period {period} and team {team}")

    