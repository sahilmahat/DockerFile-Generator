from fastapi import APIRouter
from services.analyzer import CodeAnalyzer
from services.dockerfile_generator import DockerfileGenerator
from services.ai_services import generate_dockerfile
from services.github_service import clone_repo


router=APIRouter()

@router.post("/analyzer")
async def analyze_repo(repo_path: str):
    analyzer = CodeAnalyzer(repo_path)
    language= analyzer.detect_language()
    framework = analyzer.detect_framework()
    dependencies=analyzer.get_dependencies()

    dockerfile= generate_dockerfile(language, framework, dependencies)

    return{
        "repo_path": repo_path,
        "language": language,
        "framework": framework,
        "dockerfile": dockerfile
    }

@router.post("/analyze-github")
async def analyze_github_repo(access_token: str, repo_full_name: str):
    clone_path = clone_repo(access_token, repo_full_name)
    
    analyzer = CodeAnalyzer(clone_path)
    language = analyzer.detect_language()
    
    SUPPORTED_LANGUAGES = ["python", "javascript", "go", "java"]

    if language == "unknown" or language not in SUPPORTED_LANGUAGES:
        return {
            "repo": repo_full_name,
            "error": f"'{language}' is not supported yet. We support Python, JavaScript, Go and Java."
        }
    
    framework = analyzer.detect_framework()
    dependencies = analyzer.get_dependencies()
    
    dockerfile = generate_dockerfile(language, framework, dependencies)
    
    return {
        "repo": repo_full_name,
        "language": language,
        "framework": framework,
        "dockerfile": dockerfile
    }