import os
class CodeAnalyzer:
    def __init__(self, repo_path):
        self.repo_path=repo_path

        def languages(self):
            files=os.listdir(self.repo_path)

            if "requirement.txt" in files:
                return "python"
            elif "packange.json" in files:
                return "javascript"
            elif "go.mod" in files:
                return "go"
            elif "pom.xml" in files:
                return "java"
            else:
                return "Unknown"
            