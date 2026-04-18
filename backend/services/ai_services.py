from groq import Groq
from config import settings

client=Groq(api_key=settings.groq_api_key)

def generate_dockerfile(language,framework, dependencies):
    prompt = f"""You are a DevOps expert. Generate a production-ready Dockerfile for this project:

Language: {language}
Framework: {framework}
Dependencies: {dependencies}

Rules:
- Use slim base images
- Add non-root user for security
- Use layer caching properly
- Add health check
- Add helpful comments

Return ONLY the Dockerfile content, nothing else. """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role":"user","content":prompt}
        ]
    )

    result  = response.choices[0].message.content
    result = result.replace("```dockerfile", "").replace("```", "").strip()
    return result


