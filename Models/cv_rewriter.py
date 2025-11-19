import subprocess

def run_ollama(prompt, model="llama3.1"):
    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return result.stdout.decode().strip()

def rewrite_bullet_point(bullet_point: str, job_description: str):
    prompt = f"""
    Rewrite the following CV bullet point to be more professional,
    action-oriented, concise, and tailored to this job description.

    IMPORTANT:
    - Return ONLY the rewritten bullet point.
    - No explanations.
    - No markdown.
    - No quotes.
    - One clean sentence.

    Bullet:
    {bullet_point}

    Job:
    {job_description}

    Rewritten bullet point:
    """

    return run_ollama(prompt)


if __name__ == "__main__":
    bullet = "I helped customers in the store."
    job = "Looking for customer service skills and ability to handle complaints."

    print("Rewritten:", rewrite_bullet_point(bullet, job))
