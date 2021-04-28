import sys, re
from typing import List, Union
from check import is_issue_closed

TARGET = "https://github.com/([^/]*)/([^/]*)/issues/(\d*)"

def main():
    file_path, line, target_info = split_grep_result(sys.argv[1])
    print(file_path, line, target_info)

    if is_issue_closed(target_info[0], target_info[1], target_info[2]):
        print("this issue is closed")


"""
split grep_result
return file_path, line, target_info

ex)
input ./test/Dockerfile:2:# https://github.com/shin-shin-01/github-test/issues/2
return ./test/Dockerfile, 2, ( shin-shin-01, github-test, 2 )
"""
def split_grep_result(grep_result: str) -> List[Union[str, str, str]]:
    # ファイルのパスと行数を取得
    filepath_line_split = re.findall('([^:]*):([^:]*)', grep_result)
    # ターゲットとなるパスを取得
    # - 取得条件が変化する可能性があるため個別に取得
    # - 複数存在する場合はひとつめのみ取得
    target_info = re.findall(f'{TARGET}', grep_result)

    return filepath_line_split[0][0], filepath_line_split[0][1], target_info[0]


if __name__ == "__main__":
    print("hello, world in python")
    main()
