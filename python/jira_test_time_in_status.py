#!/usr/local/bin/python3

from jira import JIRA
from util import get_settings, hours_between
from jira_report import get_numbers_for_time_spend_for_status, getTimeSpentIn
import sys

settings = get_settings()
options = { 'server': settings["jira"]["server"] }
jira = JIRA(options, basic_auth=(settings["jira"]["user"], settings["jira"]["password"]))

issues = jira.search_issues("key = CLM-10571")

for issue in issues:
    print(getTimeSpentIn(jira, issue, "In Development"))

#print(get_numbers_for_time_spend_for_status(jira, issues, "In Development"), sep=", ")

#print(hours_between("2018-08-02T17:52:46.898+0000", "2018-07-31T17:03:35.621+0000"))