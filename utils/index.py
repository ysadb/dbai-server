import json
import os
import aiohttp
from dotenv import load_dotenv
import json5

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_KEY")

if OPENAI_API_KEY == None:
    raise Exception("OPENAI_KEY not found in .env file")


async def post_request(url, headers, data=None, timeout=90):
    async with aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=timeout)
    ) as session:
        async with session.post(
            url, headers=headers, data=None if data == None else json.dumps(data)
        ) as response:
            response_json = await response.json()
            return response_json


async def get_completion(
    systemPrompt,
    messages,
    function_schema,
    function_name,
    temperature=1,
    model="gpt-3.5-turbo",
):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }

    data = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": systemPrompt,
            },
            *messages,
        ],
        "functions": [function_schema],
        "temperature": temperature,
        "function_call": {
            "name": function_name,
        },
    }

    print(json.dumps(data, indent=4, sort_keys=True))
    # Use it like this
    completion = await post_request(
        "https://api.openai.com/v1/chat/completions", headers, data
    )
    argumentsJson = completion["choices"][0]["message"]["function_call"]["arguments"]

    return json5.loads(argumentsJson)


def script_pretty_print(script):
    for index, scene in enumerate(script["scenes"]):
        print(f"Scene {index + 1}")
        print(f"Title: {scene['title']}")
        print(f"Location: {scene['location']['name']}")
        print("")
        for conversation in scene["conversation"]:
            print(f"{conversation['character']}: {conversation['dialogue']}")
        print("\n")
