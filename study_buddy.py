import os
import sys

from dotenv import load_dotenv
from mistralai.client import Mistral  # in older SDKs: from mistralai import Mistral

MODEL = "mistral-small-latest"
SYSTEM_PROMPT = (
    "You are Study Buddy, a patient and supportive tutor. Explain concepts simply, "
    "with short examples, and encourage the student. If you are not sure, say so "
    "instead of inventing facts."
)


def ask(client, messages, question):
    """Append the question, call the API, append and return the reply.
    On failure the question is removed again so history stays valid."""
    messages.append({"role": "user", "content": question})
    try:
        resp = client.chat.complete(
            model=MODEL, messages=messages, temperature=0.3, max_tokens=500
        )
    except Exception as e:
        messages.pop()
        status = getattr(e, "status_code", None)
        if status == 401:
            return "Authentication failed. Check MISTRAL_API_KEY in .env."
        if status == 429:
            return "Rate limit reached. Wait a moment and try again."
        return f"Sorry, something went wrong ({e}). Please try again."
    reply = resp.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    return reply


def main():
    load_dotenv()
    key = os.getenv("MISTRAL_API_KEY")
    if not key or key == "your-real-key-here":
        sys.exit("Error: MISTRAL_API_KEY is missing. Add it to .env (see .env.example).")
    client = Mistral(api_key=key)
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    print("Study Buddy ready. Type 'quit' or 'exit' to leave.")
    while True:
        try:
            q = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if q.lower() in ("quit", "exit"):
            break
        if q:
            print(f"\nStudy Buddy: {ask(client, messages, q)}")
    print("Good luck with your studies!")


if __name__ == "__main__":
    main()
