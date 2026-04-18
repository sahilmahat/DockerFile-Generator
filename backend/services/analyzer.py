import os
class CodeAnalyzer:
    def __init__(self, repo_path):
        self.repo_path=repo_path

    def detect_language(self):
        files=os.listdir(self.repo_path)

        if "requirements.txt" in files:
            return "python"
        elif "package.json" in files:
            return "javascript"
        elif "go.mod" in files:
            return "go"
        elif "pom.xml" in files:
            return "java"
        else:
            return "Unknown"

    def detect_framework(self):
        language = self.detect_language()

        if language == "python":
            req_file = os.path.join(self.repo_path, "requirements.txt")
            with open(req_file, "r") as f:
                content = f.read().lower()

            if "fastapi" in content:
                return "fastapi"
            elif "django" in content:
                return "django"
            elif "flask" in content:
                return "flask"
            else:
                return "plain python"

        elif language == "javascript":
            pkg_file = os.path.join(self.repo_path, "package.json")
            with open(pkg_file, "r") as f:
                content = f.read().lower()

            if "next" in content:
                return "nextjs"
            elif "express" in content:
                return "express"
            elif "react" in content:
                return "react"
            else:
                return "plain javascript"

        elif language == "go":
            go_file = os.path.join(self.repo_path, "go.mod")
            with open(go_file, "r") as f:
                content = f.read().lower()

            if "gin-gonic" in content:
                return "gin"
            elif "fiber" in content:
                return "fiber"
            else:
                return "plain go"

        elif language == "java":
            pkg_file = os.path.join(self.repo_path, "pom.xml")
            with open(pkg_file, "r") as f:
                content = f.read().lower()

            if "spring-boot" in content:
                return "springboot"
            else:
                return "plain java"

        else:
            return "unknown"            

    def get_dependencies(self):
        language=self.detect_language()

        if language=="python":
            req_file=os.path.join(self.repo_path, "requirements.txt")
            with open(req_file,"r") as f:
                return f.read()

        elif language == "javascript":
            pkg_file = os.path.join(self.repo_path, "package.json")
            with open(pkg_file, "r") as f:
                return f.read()
        
        else:
            return "unknown"
            
        