import re
import requests
from typing import List, Union

"""
split grep_result
return file_path, line, target_info

ex)
input ./test/Dockerfile:2:# https://github.com/shin-shin-01/github-test/issues/2
return ./test/Dockerfile, 2, ( shin-shin-01, github-test, 2 )
"""
def split_grep_result(TARGET: str, grep_result: str) -> List[Union[str, int, str]]:
    # ファイルのパスと行数を取得
    filepath_line_split = re.findall('([^:]*):([^:]*)', grep_result)
    # ターゲットとなるパスを取得
    # - 取得条件が変化する可能性があるため個別に取得
    # - 複数存在する場合はひとつめのみ取得
    target_info = re.findall(f'{TARGET}', grep_result)

    return filepath_line_split[0][0], int(filepath_line_split[0][1]), target_info[0]


"""
ISSUE が CLOSE されているかの確認
"""
def is_issue_closed(owner: str, repo: str, number: str) -> bool:
    response = requests.get(f'https://api.github.com/repos/{owner}/{repo}/issues/{number}')

    if response.status_code != 200: return False

    response = response.json()
    state = response['state']

    # closed_at = response['closed_at']
    
    return state == 'closed'


"""
修正できる箇所に コメント '# this may be fixed!' を挿入する
"""
def edit_code(file_path: str, line: int) -> None:
    #ファイルをリストで読み込み
    with open(file_path)as f:
        data = f.readlines()

    data.insert(line, '# this may be fixed!\n')

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
    data.pop(line)

    #元のファイルに書き込み
    with open(file_path, mode='w')as f:
        f.writelines(data)
