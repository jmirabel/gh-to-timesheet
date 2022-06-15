import typing as T
import os
import json

class GHError(Exception):
    def __init__(self, msg, data):
        super().__init__(msg)
        self.data = data

class GH:
    def __init__(self, org="eurekarobotics", repo="eureka", verbose = False):
        self._org = org
        self._repo = repo
        self._verbose = verbose

        self.def_opts = [
            #"--include",
            "--header", "\"Accept: application/vnd.github.v3+json\"",
            "--cache", "3600s",
        ]

    @property
    def basereq(self):
        return f"repos/{self._org}/{self._repo}"

    def repo_api(self, what: str, options: T.List[str] = []):
        return self.api(f"{self.basereq}/{what}", options)

    def api(self, what: str, options: T.List[str] = []):
        opt_str = " ".join(self.def_opts + options)
        if self._verbose:
            print(f"gh api {opt_str} {what}")
        ostream = os.popen(f"gh api {opt_str} {what}")
        output = ostream.read()
        try:
            data = json.loads(output)
        except json.JSONDecodeError as e:
            raise GHError(e, output)
        if isinstance(data, dict) and "documentation_url" in data.keys():
            raise GHError("GH request failed.", output)
        return data

    def pulls(self, options: T.List[str] = []):
        return self.repo_api("pulls", options)

    def issues(self, options: T.List[str] = []):
        return self.repo_api("issues", options)

    def search_issues(self, options: T.List[str] = []):
        return self.api("/search/issues", [ "-X", "GET" ] + options)
    
    def pull(self, number: T.Union[int,str]):
        return self.repo_api(f"pulls/{number}")

    def issue(self, number: T.Union[int,str], options: T.List[str] = []):
        return self.repo_api(f"issues/{number}", options)
    
    def pull_commits(self, number: T.Union[int,str]):
        return self.repo_api(f"pulls/{number}/commits")
