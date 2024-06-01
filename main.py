import asyncio
from api.prompt.script import generateScript
from utils.index import script_pretty_print


async def main():
    topic = input("Enter a topic: ")
    topicplus = input("topicplus? (uses gpt4o) (y/n): ") == "y"
    result = await generateScript(topic, {}, 101 if topicplus else 0)
    script_pretty_print(result)


asyncio.run(main())
