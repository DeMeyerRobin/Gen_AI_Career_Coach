import subprocess

def run_ollama(prompt, model="llama3.1"):
    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return result.stdout.decode().strip()

def generate_questions(job_title: str, n=5):
    prompt = f"""
    Generate {n} professional interview questions for the job: {job_title}.
    
    Rules:
    - Return ONLY the questions.
    - Use a numbered list (1., 2., 3., …).
    - No explanations.
    """

    return run_ollama(prompt)

if __name__ == "__main__":
    print(generate_questions("Software Engineer"))
