#!/usr/local/bin/python3

from jira import JIRA
from util import get_settings
from models.IssueType import IssueType
from models.TeamReport import TeamReport
from jira_utils import get_numbers_for_time_spend_for_status, get_transition_counts_for_issues
import sys

settings = get_settings()
options = { 'server': settings["jira"]["server"] }
jira = JIRA(options, basic_auth=(settings["jira"]["user"], settings["jira"]["password"]))

policyJQL = 'project = CLM AND fixVersion = [VER] AND statusCategory = Done AND type = Bug AND summary ~ "Nexus IQ:" AND Team = [TEAM]'
bugJQL = 'project = CLM AND fixVersion = [VER] AND statusCategory = Done AND type = Bug AND summary !~ "Nexus IQ:" AND Team = [TEAM]'
storyJQL = 'project = CLM AND fixVersion = [VER] AND statusCategory = Done AND type = Story AND Team = [TEAM]'
techDebtJQL = 'project = CLM AND fixVersion =[VER] AND statusCategory = Done AND type = "Technical Debt" AND Team = [TEAM]'

issueTypes = [IssueType(bugJQL, "Bugs"),
                IssueType(policyJQL, "Policy Violations"), 
                IssueType(storyJQL, "Story"), 
                IssueType(techDebtJQL, "Tech Debt")]

# set version
if len(sys.argv) > 1:
    version = sys.argv[1]
else:
    print("running with default version of Joy")
    version = 'Joy'

teamReports = [TeamReport(17), TeamReport(35), TeamReport(36), TeamReport(38)]
teams = [17,35,36,38]

print(version)
print("team, type, total issues")
print("transition, count")

# loop over each team
for team in teamReports:
    team.release = version
    ## collect data
    for issueType in issueTypes:
        issues = issueType.get_jira_issues(jira, version, team)
        transitions = get_transition_counts_for_issues(jira, issues)
        for k in transitions:
            print(team.team_id, issueType.issueType, len(issues), sep=", ", end=", ")
            print(k.split(":")[0], k.split(":")[1], sep=", ", end=", ")
            print(transitions[k], sep=", ")

