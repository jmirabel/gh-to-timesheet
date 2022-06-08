class Timesheet:
    def __init__(self):
        self._prs = dict()
        self._records = dict()
        self._repo = None

    def _record(self, name, date):
        r_for_user = self._records.setdefault(name, {})
        r_for_user_for_date = r_for_user.setdefault(date, {})
        return r_for_user_for_date

    @property
    def repo(self):
        return self._repo

    @repo.setter
    def repo(self, repo: str):
        self._repo = repo

    def add_pr(self, pr_number, title):
        assert (self.repo,pr_number) not in self._prs, f"PR {self.repo}/{pr_number} already registered"
        self._prs[(self.repo,pr_number)] = title

    def add_record(self, name, date, pr_number):
        assert (self.repo,pr_number) in self._prs, "PR not registered"
        record = self._record(name, date)
        key = (self.repo, pr_number)
        if key in record:
            record[key] += 1
        else:
            record[key] = 1

    def print_summary(self):
        for name, records in self._records.items():
            print(name)
            for date, record in records.items():
                total = sum(record.values())
                print(f"  {date.isoformat()}: ", ", ".join(
                    f"{repo}/{pr_number} ({int(100*count/total)}%)" for (repo,pr_number), count in record.items()
                ))
