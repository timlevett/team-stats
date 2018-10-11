#!/usr/local/bin/python3

from jira_report import print_jira_info
from github_report import get_pull_request_information
from util import get_settings

settings = get_settings()

print("---jira info---")
issueKeys = print_jira_info(settings)

print()
print('---pr info---')
get_pull_request_information(settings, issueKeys)