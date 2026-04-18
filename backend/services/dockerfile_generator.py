class DockerfileGenerator:
    def __init__(self, language, framework):
        self.language=language
        self.framework=framework
        
    def generate(self):
        if self.language == "python":
            return self.python_dockerfile()
        else:
            return "not yet supported for this type of language"

    def python_dockerfile(self):
        framework = self.framework.lower()
        if self.framework == "fastapi":
            return """FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
        elif self.framework == "django":
            return """FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
"""
        elif self.framework == "flask":
            return """FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]
"""
        else:
            return """FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]
"""
