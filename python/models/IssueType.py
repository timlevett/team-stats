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