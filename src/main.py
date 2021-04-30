import sys
from func import split_grep_result, is_issue_closed, is_new_version_released, edit_code, revert_code
from git import GitClass

def main():
    git_token = sys.argv[1]
    git_owner_repo = sys.argv[2].split("/")
    default_branch = sys.argv[3]
    target_type = sys.argv[4]

    file_path, line, target_info = split_grep_result(target_type, sys.argv[5])
    print(file_path, line, target_info)
    

    """
    notify の条件確認
    """
    if target_type == "issue":
        if not is_issue_closed(owner=target_info[0], repo=target_info[1], number=target_info[2]):
            print("this issue is 'still opened' or 'closed at more than a day ago'.")
            return
    else:
        if not is_new_version_released(owner=target_info[0], repo=target_info[1]):
            print("new version is 'not released' or 'released at more than a day ago'.")
            return


    """
    修正できる箇所に コメント '# this may be fixed!' を挿入する
    """
    edit_code(file_path=file_path, line=line)

    """
    Git: ブランチ作成 / コミット作成 / PR作成
    """
    git = GitClass(owner=git_owner_repo[0], repo=git_owner_repo[1], base_branch=default_branch, git_token=git_token)

    try:
        print("start GitAction")
        base_sha = git.GetBaseSha()
        print("done GetBaseSha")
        git.CreateBranch(base_sha=base_sha)
        print("done CreateBranch")
        content_sha = git.GetContentSha(file_path=file_path)
        print("done GetContentSha")
        git.PushToGitHub(file_path=file_path, content_sha=content_sha)
        print("done PushToGitHub")
        git.CreatePullRequest()
        print("done CreatePullRequest")
    except Exception:
        print('Faild...')

    """
    挿入したコメント '# this may be fixed!' を削除する
    """
    revert_code(file_path=file_path, line=line)

    print("Done! notifyAction")

if __name__ == "__main__":
    print("hello, world in python")
    main()
