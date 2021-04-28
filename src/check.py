import requests

"""
ISSUE が CLOSE されているかの確認
"""
def is_closed_issue(owner: str, repo: str, number: str) -> bool:
    response = requests.get(f'https://api.github.com/repos/{owner}/{repo}/issues/{number}')

    if response.status_code != 200: return False

    response = response.json()
    state = response['state']

    # closed_at = response['closed_at']
    
    return state == 'closed'
