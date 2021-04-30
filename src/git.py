import json
from typing import Dict
import requests
import base64
from datetime import datetime

"""
- GetBaseSha
- CreateBranch: base_sha
- GetContentSha: file_path
- PushToGitHub: file_path, content_sha
- CreatePullRequest
"""
class GitClass:
    owner = ""
    repo = ""
    base_branch = ""
    head_branch = ""
    git_token = ""
    

    def __init__(self, owner: str, repo: str, base_branch: str, git_token: str):
        self.owner = owner
        self.repo = repo
        self.base_branch = base_branch
        self.git_token = git_token

        self.head_branch = self.__createHeadBranchName()


    """
    create a unique branch name from datetime
    """
    def __createHeadBranchName(self) -> str:
        now = datetime.now()
        # 毎日定刻に実行するため日付と秒で一意にする
        # ex) '2021043047'
        now_str = now.strftime("%Y%m%d%S")

        return f"notifyaction/{now_str}"


    """
    header to request github.api
    """
    def __header(self) -> Dict:
        return {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {self.git_token}"
        }

    """
    return refs/heads/base SHA
    """
    def GetBaseSha(self) -> str:
        git_refs_api = f"https://api.github.com/repos/{self.owner}/{self.repo}/git/refs/heads/{self.base_branch}"

        response = requests.get(
            git_refs_api,
            headers = self.__header,
        )

        if not response.ok:
            print(f"Request Failed: {response.text}")
            raise Exception

        base_sha = response.json()['object']['sha']

        return base_sha


    """
    create Branch
    """
    def CreateBranch(self, base_sha: str) -> None:
        git_refs_api = f"https://api.github.com/repos/{self.owner}/{self.repo}/git/refs"

        payload = {
            "ref": f"refs/heads/{self.head_branch}",
            "sha": base_sha
        }

        response = requests.post(
            git_refs_api,
            headers = self.__header,
            data=json.dumps(payload)
        )

        if not response.ok:
            print(f"Request Failed: {response.text}")
            raise Exception

    """
    return contents/file?ref=base SHA
    """
    def GetContentSha(self, file_path: str) -> str:
        git_content_url = f"https://api.github.com/repos/{self.owner}/{self.repo}/contents/{file_path}?ref={self.base_branch}"

        response = requests.get(
            git_content_url,
            headers = self.__header
        )

        if not response.ok:
            print(f"Request Failed: {response.text}")
            raise Exception

        content_sha = response.json()['sha']

        return content_sha


    """
    create commit and push to github
    """
    def PushToGitHub(self, file_path: str, content_sha: str) -> None:
        git_content_url = f"https://api.github.com/repos/{self.owner}/{self.repo}/contents/{file_path}"
    
        base64content = base64.b64encode(open(file_path, "rb").read())

        payload = ({
            "message":"commit message",
            "branch": self.head_branch,
            "content": base64content.decode("utf-8") ,
            "sha": content_sha
        })

        response = requests.put(
            git_content_url,
            headers = self.__header,
            data = json.dumps(payload),
        )

        if not response.ok:
            print(f"Request Failed: {response.text}")
            raise Exception

    """
    create PullRequest
    """
    def CreatePullRequest(self) -> None:
        git_pulls_api = f"https://api.github.com/repos/{self.owner}/{self.repo}/pulls"

        payload = {
            "title": "title",
            "body": "body",
            "head": f"{self.owner}:{self.head_branch}",
            "base": self.base_branch,
        }

        response = requests.post(
            git_pulls_api,
            headers = self.__header,
            data = json.dumps(payload)
        )

        if not response.ok:
            print(f"Request Failed: {response.text}")
            raise Exception
    
