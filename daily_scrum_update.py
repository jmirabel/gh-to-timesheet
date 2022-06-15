import sys
import gh_to_timesheet.gh
import gh_to_timesheet.timesheet
import dateutil.parser

username="jmirabel"
if len(sys.argv) > 2:
    print("Usage: daily_scrum_update.py [username]")
    sys.exit(1)
elif len(sys.argv) == 2:
    username = sys.argv[1]

gh_ek = gh_to_timesheet.gh.GH()
gh_dm = gh_to_timesheet.gh.GH(repo="deep_models")

def print_sep():
    #print("-----------------------------")
    pass

print("""# What I did yesterday
See previously
""")

print("# What I work on today")
show_pulls = False
pr_with_review_request = []
for gh in (gh_ek, gh_dm):
    print(f"\nIssues ({gh._repo}):")
    issues = gh.issues(['-X', 'GET', '-f', f'assignee={username}'])
    for issue in issues:
        n = issue['number']
        print(f"- [{n}]({issue['html_url']}): {issue['title']}")

    if show_pulls:
        print(f"\nPR ({gh._repo}):")
    pulls = gh.pulls()
    for pull in pulls:
        if pull["user"]["login"] == username:
            n = pull['number']
            if show_pulls:
                print(f"- [{n}]({pull['html_url']}): {pull['title']}")
            if len(pull["requested_reviewers"]) > 0:
                pr_with_review_request.append(pull)

print("\n# What is in my way")
if len(pr_with_review_request) == 0:
    print("Nothing")
else:
    msg = "- Awaiting review of"
    for pull in pr_with_review_request:
        msg += f"\n  - [{pull['number']}]({pull['html_url']}) by "
        for reviewer in pull["requested_reviewers"]:
            msg += reviewer["login"]
    print(msg)

print("""
# I am going to finish everything assigned to me in this sprint?
Maybe
""")
