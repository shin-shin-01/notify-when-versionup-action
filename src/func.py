import re
import requests
from typing import Dict, List, Union, Tuple
from datetime import datetime

TARGET = {
    "issue": "https://github.com/([^/]*)/([^/]*)/issues/(\d*)",
    "release": "https://github.com/([^/]*)/([^/]*)/releases"
}

"""
split grep_result
return file_path, line, target_info

ex)
input ./test/Dockerfile:2:# https://github.com/shin-shin-01/github-test/issues/2
return ./test/Dockerfile, 2, ( shin-shin-01, github-test, 2 )
"""
def split_grep_result(target_type: str, grep_result: str) -> List[Union[str, int, Tuple[str, ...]]]:
    # ファイルのパスと行数を取得
    filepath_line_split = re.findall('([^:]*):([^:]*)', grep_result)
    # ターゲットとなるパスを取得
    # - 取得条件が変化する可能性があるため個別に取得
    # - 複数存在する場合はひとつめのみ取得
    target_info = re.findall(TARGET[target_type], grep_result)

    return filepath_line_split[0][0], int(filepath_line_split[0][1]), target_info[0]


"""
ISSUE が CLOSE されているかの確認
- 24時間以内にCLOSEされていたらPR作成を行う
"""
def is_issue_closed(owner: str, repo: str, number: str) -> Union[bool, Dict]:
    response = requests.get(f'https://api.github.com/repos/{owner}/{repo}/issues/{number}')

    if not response.ok: return False

    response = response.json()
    state = response['state']

    if state != 'closed': return False

    closed_at = response['closed_at']
    datetime_closed_at = datetime.strptime(closed_at, "%Y-%m-%dT%H:%M:%SZ")
    now = datetime.now()
    
    # ISSUE が closed かつ closed_at との時間差が 1日以内であれば Response を返す
    return response if (now - datetime_closed_at).days < 1 else False

"""
新しいバージョンがリリース されているかの確認
- 24時間以内にリリースされていたらPR作成を行う
"""
def is_new_version_released(owner: str, repo: str) -> Union[bool, Dict]:
    response = requests.get(f'https://api.github.com/repos/{owner}/{repo}/releases/latest')

    if not response.ok: return False

    response = response.json()
    published_at = response['published_at']
    datetime_published_at = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")
    now = datetime.now()

    # published_at との時間差が 1日以内であれば Response を返す
    return response if (now - datetime_published_at).days < 1 else False


"""
修正できる箇所に コメント '# this may be fixed!' を挿入する
"""
def edit_code(file_path: str, line: int) -> None:
    #ファイルをリストで読み込み
    with open(file_path)as f:
        data = f.readlines()

    data.insert(line - 1, '# this may be fixed!\n')

    #元のファイルに書き込み
    with open(file_path, mode='w')as f:
        f.writelines(data)

"""
挿入した '# this may be fixed!' を削除する
"""
def revert_code(file_path: str, line: int) -> None:
    #ファイルをリストで読み込み
    with open(file_path)as f:
        data = f.readlines()

    #挿入したコメントを削除
    data.pop(line - 1)

    #元のファイルに書き込み
    with open(file_path, mode='w')as f:
        f.writelines(data)


"""
issue クローズ時の PR内容
"""
def get_issue_pr_message(issue: Dict) -> Dict:
    repo_issue_num = re.findall(f"https://github.com/(.*)", issue['html_url'])[0]

    title = f"notify: {repo_issue_num} is closed."
    body = f"""
    {repo_issue_num} is closed.

    >> "{issue['title']}"
    >
    > {issue['body']}

    see here: {issue['html_url']}
    closed at: {issue['closed_at']}

    Please check.
    """

    body = text_format(body)
    return { "title": title, "body": body }

"""
new version リリース時の PR内容
"""
def get_release_pr_message(release: Dict) -> Dict:
    repo = re.findall(f"https://github.com/(.*)/releases/tag/{release['tag_name']}", release['html_url'])[0]

    title = f"notify: {repo}'s new version `{release['tag_name']}` is released."
    body = f"""
    {repo}: new version `{release['tag_name']}` is released.

    ReleaseNote
    > {release['body']}

    see here: {release['html_url']}
    published at: {release['published_at']}

    Please check.
    """

    body = text_format(body)
    return { "title": title, "body": body }


"""
複数行文章の最初の空白を削除する関数
"""
def text_format(text: str) -> str:
    text = map(lambda txt: txt.lstrip(), text.splitlines())
    text = list(text)[1:] # 最初の行の空白を削除
    return '\n'.join(text)
