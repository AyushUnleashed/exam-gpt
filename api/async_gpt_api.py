import os
from dotenv import find_dotenv, load_dotenv
from api.prompts import BASE_PROMPT
import requests
import json
import httpx
import openai
import asyncio
from api.models import MODEL_GPT_35_TURBO
from api.logging_config import setup_logging
import time

logger = setup_logging()

# Load environment variables from the root .env file
root_env_path = find_dotenv()
load_dotenv(root_env_path)

OPENAI_API_KEY = os.getenv("OPEN_AI_API_KEY")
# client = OpenAI(api_key=OPENAI_API_KEY)


SYSTEM_PROMPT = BASE_PROMPT


async def fetch_async_openai_response(user_prompt: str, session: httpx.AsyncClient, index) -> str:
    try:
        chat_history = []
        chat_history.append({"role": "system", "content": SYSTEM_PROMPT})
        chat_history.append({"role": "user", "content": user_prompt})
        logger.info(f"Waiting for OpenAI response... Req:{index}")

        # response = await send_api_request(chat_history=chat_history,session=session)
        url = "https://api.openai.com/v1/chat/completions"

        MODEL_NAME = MODEL_GPT_35_TURBO
        data = json.dumps({
            "model": MODEL_NAME,
            "messages": chat_history,
            "temperature": 0.5,
        })

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
        start_single_api_await_time = time.time()
        response = await session.post(url, data=data, headers=headers)
        end_single_api_await_time = time.time()
        elapsed_single_api_await_time = round(end_single_api_await_time - start_single_api_await_time, 2)

        if response.status_code == 200:
            openai_response = response.json()
            reply = openai_response['choices'][0]['message']['content']
            completion_tokens = openai_response['usage']['completion_tokens']
            prompt_tokens = openai_response['usage']['prompt_tokens']
            total_tokens = openai_response['usage']['total_tokens']

            # print("OpenAI Paid API reply:", reply)
            # print("Completion tokens:", completion_tokens)
            # print("Prompt tokens:", prompt_tokens)
            # print("Total tokens used:", total_tokens)
            # print("Response received.")

            if elapsed_single_api_await_time > 20:
                logger.warning(f" Req: {index} took {elapsed_single_api_await_time} seconds to get response")
                # #Logging rate limit headers for better debugging
                # rate_limit_info = {
                #     "x-ratelimit-limit-requests": response.headers.get("x-ratelimit-limit-requests"),
                #     "x-ratelimit-remaining-requests": response.headers.get("x-ratelimit-remaining-requests"),
                #     "x-ratelimit-reset-requests": response.headers.get("x-ratelimit-reset-requests"),
                #     "x-ratelimit-limit-tokens": response.headers.get("x-ratelimit-limit-tokens"),
                #     "x-ratelimit-remaining-tokens": response.headers.get("x-ratelimit-remaining-tokens"),
                #     "x-ratelimit-reset-tokens": response.headers.get("x-ratelimit-reset-tokens"),
                # }
                # logger.warning(f"Req: {index} | Rate limit info: {rate_limit_info}")

            logger.info(f"Response received...Req:{index}")
            return reply, total_tokens
        elif response.status_code == 429:
            logger.error(f"Req: {index} |  429 | Rate limit exceeded. Please try again later.")
            # raise Exception("Rate limit exceeded. Please try again later.")
            return None, 0
        elif response.status_code == 500:
            logger.error(f"Req: {index} | 500 - The server had an error while processing your request")
            # raise Exception("500 - The server had an error while processing your request")
            return None, 0
        elif response.status_code == 503:
            logger.error(f"Req: {index} | 503 - The engine is currently overloaded, please try again later")
            # raise Exception("503 - The engine is currently overloaded, please try again later")
            return None, 0
        else:
            logger.error(f"Req: {index} | Error fetching response: {response.text}")
            # raise Exception(f"Error fetching response code: {response.status_code}, response: {response.text}")
            # logger.error("This shouldn't be printed")
            return None, 0

    except (openai.APIError, openai.APIConnectionError, openai.RateLimitError) as e:
        if isinstance(e, openai.RateLimitError):
            logger.error(f"Req: {index} | OpenAI API request exceeded rate limit: {e}")
        elif isinstance(e, openai.APIConnectionError):
            logger.error(f"Req: {index} | Failed to connect to OpenAI API: {e}")
        else:  # openai.APIError
            logger.error(f"Req: {index} | OpenAI API returned an API Error: {e}")
        return None, 0
        # raise e
    except Exception as e:
        logger.error(f"Req: {index}| Unhandled exception occurred while fetching response from OpenAI: {e}")
        return None, 0
        # raise e


async def main():
    async with httpx.AsyncClient() as session:
        tasks = [fetch_async_openai_response(f"User prompt {i}", session, i) for i in range(2)]
        responses = await asyncio.gather(*tasks)
        # Process responses here
        for response in responses:
            if response:
                print(response)


if __name__ == "__main__":
    asyncio.run(main())