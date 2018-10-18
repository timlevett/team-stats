from github import Github
from util import eprint

def get_pull_request_information(settings, issues):
    g = Github(settings["github_api"])

    loops = len(issues) // 5
    #print(len(issues), loops, sep=" ")

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
                        if review.state == "APPROVED":
                            approved.append(review.user.login)
                            approver_count+=1
                        else:
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

