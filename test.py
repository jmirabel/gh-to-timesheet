import gh_to_timesheet.gh
import gh_to_timesheet.timesheet
import dateutil.parser

gh = gh_to_timesheet.gh.GH()
timesheet = gh_to_timesheet.timesheet.Timesheet()

def print_sep():
    #print("-----------------------------")
    pass

for i in range(780, 824):
    try:
        pull = gh.pull(i)
    except gh_to_timesheet.gh.GHError:
        print(i, "not a PR ?")
        print_sep()
        continue
    timesheet.add_pr(i, pull['title'])
    #print(i, pull['title'], pull['state'])
    try:
        pull_commits = gh.pull_commits(i)
    except gh_to_timesheet.gh.GHError:
        print(i, "failed to fetch commits")
        print_sep()
        continue
    for pull_commit in pull_commits:
        commit = pull_commit['commit']
        committer = commit['committer']
        author = commit['author']
        cdate = dateutil.parser.isoparse(committer['date'])
        adate = dateutil.parser.isoparse(author['date'])
        l = [ (adate.date(), author['name']) ]
        if author['name'] != committer['name'] or cdate.date() != adate.date():
            l.append(( cdate.date(), committer['name'] ))
        for d, n in l:
            timesheet.add_record(n, d, i)
            #print("- ", d, n)
    print_sep()

timesheet.print_summary()
