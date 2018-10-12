#!/usr/local/bin/python3

from jira import JIRA
from util import get_settings
import sys

settings = get_settings()
options = { 'server': settings["jira"]["server"] }
jira = JIRA(options, basic_auth=(settings["jira"]["user"], settings["jira"]["password"]))

class TeamReport():
    def __init__(self, team_id):
        self.team_id = team_id
        self.release = ""
        self.issues = []
class IssueType():
    def __init__(self, jql, issueType):
        self.jql = jql
        self.issueType = issueType

    def get_scrubbed_jql(self, version, team):
        return self.jql.replace("[VER]",version).replace("[TEAM]",str(team.team_id))
    def get_jira_issues(self, jira, version, team):
        jql = self.get_scrubbed_jql(version, team)
        issues = jira.search_issues(jql)
        return issues


policyJQL = 'project = CLM AND fixVersion = [VER] AND statusCategory = Done AND type = Bug AND summary ~ "Nexus IQ:" AND Team = [TEAM]'
bugJQL = 'project = CLM AND fixVersion = [VER] AND statusCategory = Done AND type = Bug AND summary !~ "Nexus IQ:" AND Team = [TEAM]'
storyJQL = 'project = CLM AND fixVersion = [VER] AND statusCategory = Done AND type = Story AND Team = [TEAM]'
techDebtJQL = 'project = CLM AND fixVersion =[VER] AND statusCategory = Done AND type = "Technical Debt" AND Team = [TEAM]'

issueTypes = [IssueType(bugJQL, "Bugs"),
                IssueType(policyJQL, "Policy Violations"), 
                IssueType(storyJQL, "Story"), 
                IssueType(techDebtJQL, "Tech Debt")]

# set version
if sys.argv[1] is not None:
    version = sys.argv[1]
else:
    version = 'Icarus'
teamReports = [TeamReport(17), TeamReport(35), TeamReport(36), TeamReport(38)]
teams = [17,35,36,38]

# loop over each team
for team in teamReports:
    team.release = version
    ## collect data
    for issueType in issueTypes:
        issues = issueType.get_jira_issues(jira, version, team)
        team.issues.append(len(issues))

# print header
print(version, "Laurel", "Alpha", "Axon", "Atom","Total", sep=", ")

# log data
for index, iType in enumerate(issueTypes):
    tot = 0
    pstring = ""
    for team in teamReports:
        if team.team_id == 17:
            pstring += iType.issueType + ", "
        tot += team.issues[index]
        pstring += str(team.issues[index]) + ", "
        
    print(pstring, tot, sep="")
