import requests
import os
import re
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "deepseek/deepseek-r1-zero:free"
URL = "https://openrouter.ai/api/v1/chat/completions"

if not API_KEY:
    raise ValueError("OPENROUTER_API_KEY not found in environment variables.")

def query_openrouter(command):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": command}]
    }

    try:
        response = requests.post(URL, headers=headers, json=data)
        response.raise_for_status()
        response_json = response.json()

        choices = response_json.get("choices")
        if not choices or "message" not in choices[0]:
            return "Unexpected response structure from OpenRouter."

        raw_answer = choices[0]["message"]["content"].strip()

        match = re.search(r'\\boxed\{\\boxed\{?(.*?)\}?\}', raw_answer)
        if match:
            return match.group(1).strip()
        match = re.search(r'\\boxed\{(.*?)\}', raw_answer)
        if match:
            return match.group(1).strip()

        return raw_answer
    except Exception as e:
        print("OpenRouter API Error:", e)
        return "Sorry, I couldn't get an answer right now."

if __name__ == "__main__":
    while True:
        user_input = input("Enter your message (or type 'exit' to quit): ").strip()
        if user_input.lower() == "exit":
            break
        response = query_openrouter(user_input)
        print("Answer:", response)
