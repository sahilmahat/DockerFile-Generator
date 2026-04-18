import os
import shutil
from github import Github

def clone_repo(access_token, repo_full_name):
    g = Github(access_token)
    repo = g.get_repo(repo_full_name)
    
    clone_url = f"https://{access_token}@github.com/{repo_full_name}.git"
    
    clone_path = f"/tmp/{repo_full_name.replace('/', '_')}"
    
    if os.path.exists(clone_path):
        shutil.rmtree(clone_path)
    
    os.system(f"git clone {clone_url} {clone_path}")
    
    return clone_path