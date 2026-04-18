from fastapi import APIRouter
from fastapi.responses import RedirectResponse
import httpx
from config import settings

router = APIRouter()

@router.get("/login")
async def github_login():
    github_auth_url = (
        f"https://github.com/login/oauth/authorize"
        f"?client_id={settings.github_client_id}"
        f"&scope=repo"
    )
    return RedirectResponse(github_auth_url)


@router.get("/callback")
async def github_callback(code: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://github.com/login/oauth/access_token",
            data={
                "client_id": settings.github_client_id,
                "client_secret": settings.github_client_secret,
                "code": code
            },
            headers={"Accept": "application/json"}
        )
    
    data = response.json()
    access_token = data.get("access_token")
    
    if not access_token:
        return {"error": "Failed to get access token"}
    
    return {"access_token": access_token}

@router.get("/repos")
async def list_repos(access_token: str):
    from github import Github
    
    g = Github(access_token)
    user = g.get_user()
    
    repos = []
    for repo in user.get_repos():
        repos.append({
            "name": repo.name,
            "full_name": repo.full_name,
            "url": repo.html_url,
            "language": repo.language,
            "private": repo.private
        })
    
    return {"repos": repos}