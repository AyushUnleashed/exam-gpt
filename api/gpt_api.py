import os
from dotenv import find_dotenv, load_dotenv
from api.prompts import BASE_PROMPT
from api.models import MODEL_GPT_35_TURBO,MODEL_GPT_4
import requests
import json

# Load environment variables from the root .env file
root_env_path = find_dotenv()
load_dotenv(root_env_path)

OPENAI_API_KEY = os.getenv("OPEN_AI_API_KEY")
# client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = BASE_PROMPT
chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]



def reset_chat_history():
    global chat_history
    chat_history.clear()
    chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]


def set_system_prompt(NEW_PROMPT):
    global chat_history
    chat_history = [{"role": "system", "content": NEW_PROMPT}]


def fetch_openai_response(user_prompt: str):
    try:
        reset_chat_history()
        global chat_history
        chat_history.append({"role": "user", "content": user_prompt})
        print("Waiting for OpenAI response...")

        # Assuming you're using GPT-3.5 Turbo; adjust as needed
        MODEL_NAME = MODEL_GPT_4

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }

        data = json.dumps({
            "model": MODEL_NAME,
            "messages": chat_history,
            "temperature":0.5,
        })

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=data)

        if response.status_code == 200:
            openai_response = response.json()
            print(openai_response)
            reply = openai_response['choices'][0]['message']['content']
            completion_tokens = openai_response['usage']['completion_tokens']
            prompt_tokens = openai_response['usage']['prompt_tokens']
            total_tokens = openai_response['usage']['total_tokens']

            print("OpenAI Paid API reply:", reply)
            print("Completion tokens:", completion_tokens)
            print("Prompt tokens:", prompt_tokens)
            print("Total tokens used:", total_tokens)

            chat_history.append({"role": "assistant", "content": reply})
            print("Response received.")
            return reply
        else:
            print("Error fetching response:", response.text)
            return None

    except Exception as e:
        print("Exception occurred while fetching response from OpenAI:", e)
        return None
