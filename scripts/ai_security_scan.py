import os
import sys
import requests

def scan_dockerfile(dockerfile_path):
    if not os.path.exists(dockerfile_path):
        print(f"[ERROR] File not found: {dockerfile_path}")
        sys.exit(1)

    with open(dockerfile_path, "r", encoding="utf-8") as f:
        dockerfile_content = f.read()

    api_key = os.getenv("LLM_API_KEY")
    if not api_key:
        print("[ERROR] LLM_API_KEY environment variable is missing!")
        sys.exit(1)

    print("[INFO] Starting AI Security Audit on Dockerfile...")

    # Custom OpenAI-compatible API (OpenRouter/Claude)
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = f"""
    You are a strict DevSecOps Security Auditor for Enterprise Infrastructure.
    Analyze the following Dockerfile for security vulnerabilities, bad practices, and misconfigurations:

   
    {dockerfile_content}
    
    Check specifically for:
    1. Running as root user.
    2. Missing image pinning or insecure base images.
    3. Unnecessary root privileges or missing USER directive.

    Respond in EXACTLY this format:
    STATUS: [PASSED or FAILED]
    CRITICAL_ISSUES:
    - issue 1
    - issue 2
    RECOMMENDATIONS:
    - rec 1
    """

    payload = {
        "model": "google/gemini-2.5-flash-lite",  
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        result = response.json()["choices"][0]["message"]["content"]

        print("\n=== AI SECURITY AUDIT REPORT ===")
        print(result)
        print("===============================\n")

        if "STATUS: FAILED" in result:
            print("[CRITICAL] Security audit failed! Pipeline blocked.")
            sys.exit(1)
        else:
            print("[SUCCESS] Security audit passed successfully.")
            sys.exit(0)

    except Exception as e:
        print(f"[ERROR] API Request failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    scan_dockerfile("Dockerfile")
