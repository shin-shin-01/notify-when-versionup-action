import sys, re

TARGET = "https://api.github.com/repos/[^/\n]*/[^/\n]*/issues/\d*"

def main():
    file_path, line, target_path = split_grep_result(sys.argv[1])
    print(file_path, line, target_path)


"""
split grep_result
return file_path, line, target_path

ex)
input ./test/Dockerfile:2:# https://api.github.com/repos/octocat/hello-world/issues/42
return ./test/Dockerfile, 2, https://api.github.com/repos/octocat/hello-world/issues/42
"""
def split_grep_result(grep_result: str) -> list[str, str, str]:
    # ファイルのパスと行数を取得
    filepath_line_split = re.findall('([^:]*):([^:]*)', grep_result)
    # ターゲットとなるパスを取得
    # - 取得条件が変化する可能性があるため個別に取得
    # - 複数存在する場合はひとつめのみ取得
    target_path = re.findall(f'{TARGET}', grep_result)

    return filepath_line_split[0][0], filepath_line_split[0][1], target_path[0]


if __name__ == "__main__":
    print("hello, world in python")
    main()
