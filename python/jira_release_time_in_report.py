#!/usr/local/bin/python3

from jira import JIRA
from util import get_settings
from models.IssueType import IssueType
from models.TeamReport import TeamReport
from jira_utils import get_numbers_for_time_spend_for_status
from jira_sql_dao import insert_into_time_in_status
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

# set version
if len(sys.argv) > 2:
    statusToCheck = sys.argv[2]
else:
    print("running with default status to check")
    #statusToCheck = 'In Development'
    statusToCheck = 'Waiting for Review'


teamReports = [TeamReport(17), TeamReport(35), TeamReport(36), TeamReport(38)]
teams = [17,35,36,38]

# loop over each team
for team in teamReports:
    team.release = version
    ## collect data
    for issueType in issueTypes:
        issues = issueType.get_jira_issues(jira, version, team)
        team.issues.append(issues)

# print header
#print(version + " - " + statusToCheck, "Laurel", "Alpha", "Axon", "Atom", sep=", ")

# log data
statuses = [
    'Groomed'
    , 'In Development'
    , 'Raw', 
    'Ready to Develop'
    ,'Testing In Progress'
    ,'To Be Tested'
    ,'Waiting for Review'
    ,'Done'
    ,'On Hold'
    ,'Open'
    'Ready to Groom'
    ,'Create Demo']
for status in statuses:

    for index, iType in enumerate(issueTypes):
        for j, team in enumerate(teamReports):
            teamIssuesForType = team.issues[index]
            count, sum, max, min, avg, stdev, median = get_numbers_for_time_spend_for_status(jira, teamIssuesForType, status)
            insert_into_time_in_status(version, iType.issueType, team.team_id, status, count, sum, max, median, stdev)
