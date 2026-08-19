import os
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5-coder:0.5b"

IMPORTANT_FILES = [
    "package.json",
    "package-lock.json",
    "requirements.txt",
    "pyproject.toml",
    "pom.xml",
    "build.gradle",
    "go.mod",
    "Cargo.toml",
    "README.md",
    "vite.config.js",
    "next.config.js",
    "angular.json",
]

repo_content = ""

print("Scanning repository...")

for root, dirs, files in os.walk("."):
    dirs[:] = [
        d for d in dirs
        if d not in [
            ".git",
            "node_modules",
            "dist",
            "build",
            ".next",
            ".venv",
            "target",
            "__pycache__"
        ]
    ]

    for file in files:
        if file in IMPORTANT_FILES:
            path = os.path.join(root, file)

            try:
                with open(
                    path,
                    "r",
                    encoding="utf-8",
                    errors="ignore"
                ) as f:

                    content = f.read()

                    repo_content += f"\n\n===== FILE: {path} =====\n"
                    repo_content += content[:15000]

                print(f"Loaded: {path}")

            except Exception as e:
                print(f"Failed: {path} -> {e}")

print("\nExamples:")
print("- Generate a production Dockerfile")
print("- Generate docker-compose.yml")
print("- Generate Kubernetes deployment")
print("- Generate Jenkinsfile")

user_prompt = input("\nEnter your DevOps request: ")

prompt = f"""
You are a Senior DevOps Engineer.

Repository Content:

{repo_content}

Task:

{user_prompt}

STRICT RULES:

- Return ONLY the requested file content.
- No explanations.
- No markdown.
- No code fences.
- No descriptions.
- No notes.
- No bullet points.
- Output must begin immediately with the file content.
- For Dockerfile output, first line MUST start with FROM.
- Generate production-ready configuration.
- Use security best practices.
- Use multi-stage builds whenever applicable.
"""

print("\nGenerating...\n")

response = requests.post(
    OLLAMA_URL,
    json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    },
    timeout=600
)

if response.status_code != 200:
    print("Request failed:")
    print(response.text)
    exit(1)

data = response.json()

if "response" not in data:
    print("Unexpected response:")
    print(data)
    exit(1)

generated_content = data["response"].strip()

# Extract Dockerfile if model adds extra text
if "dockerfile" in user_prompt.lower():

    if "FROM " in generated_content:

        start = generated_content.find("FROM ")
        generated_content = generated_content[start:]

        if "```" in generated_content:
            generated_content = generated_content.split("```")[0]

        filename = "Dockerfile"

    else:
        print("Model did not generate a valid Dockerfile")
        print("\nResponse:\n")
        print(generated_content)
        exit(1)

elif "docker-compose" in user_prompt.lower():
    filename = "docker-compose.yml"

elif "compose" in user_prompt.lower():
    filename = "docker-compose.yml"

elif "jenkins" in user_prompt.lower():
    filename = "Jenkinsfile"

elif "kubernetes" in user_prompt.lower():
    filename = "deployment.yaml"

elif "deployment" in user_prompt.lower():
    filename = "deployment.yaml"

else:
    filename = "generated_artifact.txt"

with open(filename, "w") as f:
    f.write(generated_content)

print(f"\n✅ Generated: {filename}")

print("\nPreview:\n")
print("=" * 70)
print(generated_content[:2000])
print("=" * 70)
