class Timesheet:
    def __init__(self):
        self._prs = dict()
        self._records = dict()

    def _record(self, name, date):
        r_for_user = self._records.setdefault(name, {})
        r_for_user_for_date = r_for_user.setdefault(date, {})
        return r_for_user_for_date

    def add_pr(self, pr_number, title):
        assert pr_number not in self._prs
        self._prs[pr_number] = title

    def add_record(self, name, date, pr_number):
        assert pr_number in self._prs, "PR not registered"
        record = self._record(name, date)
        if pr_number in record:
            record[pr_number] += 1
        else:
            record[pr_number] = 1

    def print_summary(self):
        for name, records in self._records.items():
            print(name)
            for date, record in records.items():
                total = sum(record.values())
                print(f"  {date.isoformat()}: ", ", ".join(
                    f"{pr_number} ({int(100*count/total)}%)" for pr_number, count in record.items()
                ))
